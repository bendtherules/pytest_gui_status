# pytest_plugins = "pytest_gui_status.status_plugin"

import redis
import pytest
from pytest_gui_status.status_plugin.plugin import REDIS_PORT


class PYTEST_DATA(object):
    data = {}

saved_data = {
    "after_sessionstart": None,
    "after_first_collectstart": None,
    "after_last_itemcollected": None,
    "after_first_runtest_logstart": None,
    "after_this_runtest_logstart": None,
}


def get_cur_data():

    dir_name = PYTEST_DATA.data["dir_name_start"]
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
    hash_dir_name = redis_db.hget("directories_to_hash", dir_name)
    assert hash_dir_name is not None

    data = {}

    data["state"] = redis_db.get("{hash_a}_state".format(hash_a=hash_dir_name))
    data["last_updated"] = redis_db.get("{hash_a}_last_updated".format(hash_a=hash_dir_name))

    data["collect"] = redis_db.lrange("{hash_a}_collect".format(hash_a=hash_dir_name), 0, -1)
    data["pass"] = redis_db.lrange("{hash_a}_pass".format(hash_a=hash_dir_name), 0, -1)
    data["fail"] = redis_db.lrange("{hash_a}_fail".format(hash_a=hash_dir_name), 0, -1)
    data["skip"] = redis_db.lrange("{hash_a}_skip".format(hash_a=hash_dir_name), 0, -1)

    # strip off the filename
    data["collect"] = [item.split("::")[-1] for item in data["collect"]]
    data["pass"] = [item.split("::")[-1] for item in data["pass"]]
    data["fail"] = [item.split("::")[-1] for item in data["fail"]]
    data["skip"] = [item.split("::")[-1] for item in data["skip"]]

    return data


@pytest.hookimpl(trylast=True)
def pytest_sessionstart(session):
    PYTEST_DATA.data["dir_name_start"] = str(session.startdir)

    saved_data["after_sessionstart"] = get_cur_data()


@pytest.hookimpl(trylast=True)
def pytest_collectstart(collector):
    if not saved_data["after_first_collectstart"]:
        saved_data["after_first_collectstart"] = get_cur_data()


@pytest.hookimpl(trylast=True)
def pytest_itemcollected(item):
    saved_data["after_last_itemcollected"] = get_cur_data()


@pytest.hookimpl(trylast=True)
def pytest_runtest_logstart(nodeid, location):
    if not saved_data["after_first_runtest_logstart"]:
        saved_data["after_first_runtest_logstart"] = get_cur_data()

    saved_data["after_this_runtest_logstart"] = get_cur_data()


@pytest.fixture
def status_plugin_debug():
    return saved_data
