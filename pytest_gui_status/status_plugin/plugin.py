import shlex
import subprocess
import time
import sys
import redis
import os

env_redis_port = os.environ.get("pytest_status_port")
if env_redis_port:
    REDIS_PORT = int(env_redis_port)
else:
    REDIS_PORT = 5946

command_redis_server_gen = "redis-server --port {port} --maxheap 20MB"
command_redis_server = command_redis_server_gen.format(port=REDIS_PORT)

# Redis will look like:
# PYTEST_STATUS_DB = 1
# directories_to_hash = {"dir_a":hash_a,"dir_b":hash_b}
# {hash_a}_state = "start" / "collect" / "runtest" / "end"
# {hash_a}_last_updated = 2015-12-12T20:50:16.056000 # isoformat
# output - datetime.datetime.now().isoformat()
# input - dateutil.parser.parse()
# {hash_a}_collect = [test_a_name, test_b_name,...]
# {hash_a}_pass = [test_a_name,...]
# {hash_a}_fail = [test_b_name,...]
# {hash_a}_skip = [test_c_name,...]


class Helpers(object):

    @staticmethod
    def on_start(dir_name):
        '''
        Init gui_status and redis on start of pytest.

        dir_name - Name of directory from which pytest started
        '''
        command_redis_server_args = shlex.split(command_redis_server)
        print(command_redis_server_args)

        print("Starting up redis")
        redis_popen_obj = subprocess.Popen(command_redis_server_args)

        # wait and check if redis has not exited yet
        time.sleep(1)
        if redis_popen_obj.poll() is None:
            print("Started successfully redis")
        else:
            print("Redis couldnt start there, trying to check if already running on that port")
            redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
            if redis_db.ping() and redis_db.get("PYTEST_STATUS_DB") == "1":
                print("Yup, it was already running")
            else:
                print("** Not found existing redis, couldnt connect, check! **")
                sys.exit()

        # todo : start and check gui with dir name and hash

        # craete redis connection and set sample key
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        redis_db.set("PYTEST_STATUS_DB", "1")

        hash_dir_name = hash(dir_name)
        redis_db.hset("directories_to_hash", dir_name, hash_dir_name)
        Helpers.on_start_reset(dir_name)

        redis_db.set("{hash_a}_state".format(hash_a=hash_dir_name), "start")

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_collectstart(dir_name):
        # craete redis connection
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)

        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        redis_db.set("{hash_a}_state".format(hash_a=hash_dir_name), "collect")

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_collectend(dir_name, list_test_name):
        # craete redis connection
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)

        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        redis_db.rpush("{hash_a}_collect".format(hash_a=hash_dir_name), *list_test_name)

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_test_eachstart(dir_name):
        # craete redis connection
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)

        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        redis_db.set("{hash_a}_state".format(hash_a=hash_dir_name), "runtest")

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_test_eachend(dir_name, list_test_result):
        # craete redis connection
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)

        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        list_testname_pass = [test_result.nodeid for test_result in
                              list_test_result if test_result.outcome == "passed"]

        list_testname_fail = [test_result.nodeid for test_result in
                              list_test_result if test_result.outcome == "failed"]

        list_testname_skip = [test_result.nodeid for test_result in
                              list_test_result if test_result.outcome == "skipped"]

        if list_testname_pass:
            redis_db.lpush("{hash_a}_pass".format(hash_a=hash_dir_name), *list_testname_pass)
        if list_testname_fail:
            redis_db.lpush("{hash_a}_fail".format(hash_a=hash_dir_name), *list_testname_fail)
        if list_testname_skip:
            redis_db.lpush("{hash_a}_skip".format(hash_a=hash_dir_name), *list_testname_skip)

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_end(dir_name):
        # craete redis connection
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)

        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        redis_db.set("{hash_a}_state".format(hash_a=hash_dir_name), "end")

        # set last updated
        Helpers.modify_last_updated(dir_name)

    @staticmethod
    def on_start_reset(dir_name):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        list_gen_varname = ["{hash_a}_state", "{hash_a}_last_updated", "{hash_a}_collect", "{hash_a}_pass", "{hash_a}_fail", "{hash_a}_skip"]
        list_cur_varname = [varname.format(hash_a=hash_dir_name) for varname in list_gen_varname]
        del list_gen_varname

        redis_db.delete(*list_cur_varname)

    @staticmethod
    def modify_last_updated(dir_name):
        import datetime
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        cur_iso_datetime = datetime.datetime.now().isoformat()

        redis_db.set("{hash_a}_last_updated".format(hash_a=hash_dir_name), cur_iso_datetime)


# Start here
class PYTEST_DATA(object):
    data = {}


def pytest_sessionstart(session):
    PYTEST_DATA.data["dir_name_start"] = session.startdir
    Helpers.on_start(PYTEST_DATA.data["dir_name_start"])


def pytest_collectstart(collector):
    Helpers.on_collectstart(PYTEST_DATA.data["dir_name_start"])


def pytest_itemcollected(item):
    Helpers.on_collectend(PYTEST_DATA.data["dir_name_start"], [item.nodeid])


def pytest_runtest_logstart(nodeid, location):
    Helpers.on_test_eachstart(PYTEST_DATA.data["dir_name_start"])


def pytest_runtest_logreport(report):
    if report.when == "call":
        Helpers.on_test_eachend(PYTEST_DATA.data["dir_name_start"], [report])


def pytest_sessionfinish(session, exitstatus):
    Helpers.on_end(PYTEST_DATA.data["dir_name_start"])

# pytest_sessionstart(session)
# pytest_collectstart(collector) | collector.config
# pytest_itemcollected
## pytest_collection_modifyitems(session, config, items)
# pytest_collectreport
# pytest_runtest_logstart(nodeid, location) - single test start
# pytest_runtest_logreport(report) - single test end
# pytest_sessionfinish(session, exit_status) - session end
