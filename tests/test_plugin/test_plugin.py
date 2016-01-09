import pytest_gui_status.status_plugin as status_plugin
import subprocess
from mock import patch
import redis

import os
from ..utils_test import create_temp_case, reload_2_3

REDIS_TEST_PORT = status_plugin.REDIS_PORT + 1
s = status_plugin.s

CASE_BASEDIR = __file__


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
def test_whole_1(tmpdir):
    '''
    Integration test
    '''
    os.chdir(os.path.dirname(__file__))
    tmpdir = str(tmpdir)
    path_case = create_temp_case("case_1", CASE_BASEDIR, tmpdir)
    os.chdir(path_case)

    assert(os.environ.get("PYTEST_STATUS_PORT") == str(REDIS_TEST_PORT))

    popen_pytest = subprocess.Popen(["py.test", "-s"], shell=True)
    popen_pytest.wait()

    dir_name = os.getcwd()
    assert (dir_name == path_case)
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    hash_dir_name = s(redis_db.hget("directories_to_hash", dir_name))

    assert (redis_db.llen("{hash_a}_pass".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_fail".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_skip".format(hash_a=hash_dir_name)) == 0)

    collected_tests = s(redis_db.lrange("{hash_a}_collect".format(hash_a=hash_dir_name), 0, -1))
    assert (collected_tests == ["test_1.py::test_pass", "test_1.py::test_fail"])


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
def test_whole_2(tmpdir):
    '''
    Integration test
    '''
    os.chdir(os.path.dirname(__file__))
    tmpdir = str(tmpdir)
    path_case = create_temp_case("case_2", CASE_BASEDIR, tmpdir)
    os.chdir(path_case)

    popen_pytest = subprocess.Popen(["py.test", "-s"], shell=True)
    popen_pytest.wait()

    # pytest.main(["-s"])

    dir_name = path_case
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    hash_dir_name = s(redis_db.hget("directories_to_hash", dir_name))

    assert (redis_db.llen("{hash_a}_pass".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_fail".format(hash_a=hash_dir_name)) == 2)
    assert (redis_db.llen("{hash_a}_skip".format(hash_a=hash_dir_name)) == 1)


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
def test_intermediate_1(tmpdir):
    '''
    Integration test
    '''
    os.chdir(os.path.dirname(__file__))
    tmpdir = str(tmpdir)
    path_case = create_temp_case("case_3", CASE_BASEDIR, tmpdir)
    os.chdir(path_case)

    popen_pytest = subprocess.Popen(["py.test", "-s"], shell=True)
    pytest_ret_code = popen_pytest.wait()

    assert pytest_ret_code == 0


@patch.dict("os.environ",
            {"REDIS_PATH": "test_redis",
             "REDIS_ARGS": "--test_arg = test_val",
             "PYTEST_STATUS_PORT": "1234"})
def test_env_redis_1():
    '''
    Test that redis config via env variables - REDIS_PATH, REDIS_ARGS, PYTEST_STATUS_PORT work as intended.
    '''

    import pytest_gui_status.status_plugin.plugin
    import pytest_gui_status.utils

    reload_2_3(pytest_gui_status.utils)
    reload_2_3(pytest_gui_status.status_plugin.plugin)
    reload_2_3(status_plugin)

    redis_cmd_final = pytest_gui_status.utils.command_redis_server
    assert(redis_cmd_final == "test_redis --port 1234 --test_arg = test_val")

    redis_cmd_final = status_plugin.command_redis_server
    assert(redis_cmd_final == "test_redis --port 1234 --test_arg = test_val")
