import pytest_gui_status.status_plugin as status_plugin
import subprocess
from mock import patch
import redis
import pytest

import os
import tempfile
import shutil

REDIS_TEST_PORT = status_plugin.REDIS_PORT + 1


class patched_chdir(object):

    """Just like chdir, but can be used in  `with` - sets back the old path at exit"""

    def __init__(self, new_path):
        self.old_path = os.getcwd()
        self.new_path = new_path

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, type, value, traceback):
        os.chdir(self.old_path)


def create_temp_case(case_name, path_tmpdir=None):
    with patched_chdir(os.path.dirname(__file__)):
        path_test_cases = os.path.abspath("testcases/")
        path_case = os.path.join(path_test_cases, case_name)

        path_tmpdir = path_tmpdir or tempfile.mkdtemp()
        path_tmpdir_case = os.path.join(path_tmpdir, case_name)
        shutil.copytree(path_case, path_tmpdir_case)

    return path_tmpdir_case


@patch.dict("os.environ",
            {"pytest_status_port": str(REDIS_TEST_PORT)})
def test_whole_1(tmpdir):
    '''
    Integration test
    '''
    os.chdir(os.path.dirname(__file__))
    tmpdir = str(tmpdir)
    path_case = create_temp_case("case_1", tmpdir)
    os.chdir(path_case)

    assert(os.environ.get("pytest_status_port") == str(REDIS_TEST_PORT))

    popen_pytest = subprocess.Popen(["py.test", "-s"], shell=True)
    popen_pytest.wait()

    # pytest.main(["-s"])

    dir_name = os.getcwd()
    assert (dir_name == path_case)
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

    assert (redis_db.llen("{hash_a}_pass".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_fail".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_skip".format(hash_a=hash_dir_name)) == 0)

    collected_tests = redis_db.lrange("{hash_a}_collect".format(hash_a=hash_dir_name), 0, -1)
    assert (collected_tests == ["test_1.py::test_pass", "test_1.py::test_fail"])


@patch.dict("os.environ",
            {"pytest_status_port": str(REDIS_TEST_PORT)})
def test_whole_2(tmpdir):
    '''
    Integration test
    '''
    os.chdir(os.path.dirname(__file__))
    tmpdir = str(tmpdir)
    path_case = create_temp_case("case_2", tmpdir)
    os.chdir(path_case)

    popen_pytest = subprocess.Popen(["py.test", "-s"], shell=True)
    popen_pytest.wait()

    # pytest.main(["-s"])

    dir_name = path_case
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

    assert (redis_db.llen("{hash_a}_pass".format(hash_a=hash_dir_name)) == 1)
    assert (redis_db.llen("{hash_a}_fail".format(hash_a=hash_dir_name)) == 2)
    assert (redis_db.llen("{hash_a}_skip".format(hash_a=hash_dir_name)) == 1)
