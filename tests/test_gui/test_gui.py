import pytest_gui_status.status_gui.utils_gui as utils_gui
import pytest_gui_status.status_plugin.plugin as status_plugin
import pytest_gui_status.utils

from mock import patch, MagicMock
import redis
import pytest
import os.path
import datetime

from ..utils_test import reload_2_3

REDIS_TEST_PORT = pytest_gui_status.utils.REDIS_PORT + 1

mock_htmlPy_module = MagicMock()
mock_htmlPy_module.Object = object
mock_htmlPy_module.Slot.return_value = (lambda func: func)


class MockTestResult(object):
    def __init__(self, nodeid, outcome):
        assert outcome in ["passed", "failed", "skipped"]
        self.nodeid = nodeid
        self.outcome = outcome


@pytest.fixture()
def redis_master(request, auto_shutdown=True):
    import pytest_gui_status.status_plugin.plugin as status_plugin

    class Redis_master_manager(object):
        dirname = None
        started = False

        @classmethod
        def init(cls, dirname):
            cls.dirname = dirname
            cls.started = True
            status_plugin.Helpers.on_start(cls.dirname)

    # stop redis master after test completion, whether passes or fails
    def fin():
        if auto_shutdown and Redis_master_manager.started:
            redis_db = redis.StrictRedis(host='localhost', port=status_plugin.REDIS_PORT, db=0)
            redis_db.shutdown()
    request.addfinalizer(fin)

    return Redis_master_manager  # provide the fixture value


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
class TestRedisFail(object):
    """test that appropriate errors are raised when redis is in incorrect state / shutdown"""

    def test_redis_fail_1(self, tmpdir):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # dont start redis. Also if redis running, stop it
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
        try:
            assert redis_db.ping()
            redis_db.shutdown()
        except redis.exceptions.ConnectionError:
            pass
        except AssertionError:
            pass

        # mock Controller requirements and app_gui.stop
        fake_app_gui = MagicMock()
        with pytest.raises(redis.exceptions.ConnectionError) as error_info:
            gui_backend.Controller(fake_app_gui).redraw()

        assert str(error_info.value) == "Cant connect to this socket. Is redis running?\n" \
            + "Stopping pytest_status_gui"

    def test_redis_fail_2(self, tmpdir, redis_master):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # start Redis
        redis_master.init(tmpdir.strpath)

        # status_plugin.Helpers.on_start(tmpdir.strpath)

        # make PYTEST_STATUS_DB value corrupt/incorrect
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
        redis_db.set("PYTEST_STATUS_DB", "0")

        # mock Controller requirements and app_gui.stop
        fake_app_gui = MagicMock()
        with pytest.raises(redis.exceptions.ConnectionError) as error_info:
            gui_backend.Controller(fake_app_gui).redraw()

        assert str(error_info.value) == "Redis is running on this port, but it is not related to pytest status\n"\
            + "Stopping pytest_status_gui"

        fake_app_gui.stop.assert_called_with()

        # auto cleanup of redis master by fixture

    def test_redis_fail_3(self, tmpdir, redis_master):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # start Redis
        redis_master.init(tmpdir.strpath)

        # delete PYTEST_STATUS_DB
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
        redis_db.delete("PYTEST_STATUS_DB")

        # mock Controller requirements and app_gui.stop
        fake_app_gui = MagicMock()

        with pytest.raises(redis.exceptions.ConnectionError) as error_info:
            gui_backend.Controller(fake_app_gui).redraw()

        assert str(error_info.value) == "Redis is running on this port, but it is not related to pytest status\n"\
            + "Stopping pytest_status_gui"

        fake_app_gui.stop.assert_called_with()

        # auto cleanup of redis master by fixture

    def test_redis_fail_4(self, tmpdir, redis_master):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # start Redis
        redis_master.init(tmpdir.strpath)

        # redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)

        # mock Controller requirements and app_gui.stop
        # provide invalid path
        fake_app_gui = MagicMock()
        fake_app_gui.dir_name = r"Invalid/Path"

        with pytest.raises(redis.exceptions.ConnectionError) as error_info:
            gui_backend.Controller(fake_app_gui).redraw()

        assert str(error_info.value) == "dir_name = {dir_name} not found in redis db".format(
            dir_name=fake_app_gui.dir_name)

        fake_app_gui.stop.assert_called_with()

        # auto cleanup of redis master by fixture


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
class TestBackendState(object):
    """docstring for TestBackendState"""

    @patch("pytest_gui_status.status_gui.utils_gui.render_template", MagicMock())
    def test_backend_state_1(self, tmpdir, redis_master):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # start Redis
        redis_master.init(tmpdir.strpath)

        # setup state
        status_plugin.Helpers.on_collectstart(tmpdir.strpath)
        status_plugin.Helpers.on_collectend(tmpdir.strpath, ["collect_1", "collect_2"])

        # mock app_gui with path
        fake_app_gui = MagicMock()
        fake_app_gui.dir_name = tmpdir.strpath

        tmp_controller = gui_backend.Controller(fake_app_gui)
        tmp_controller.redraw()

        assert tmp_controller.last_state["dir_name"] == tmpdir.strpath
        assert tmp_controller.last_state["dir_name_topfolder"] ==\
            os.path.basename(tmpdir.strpath)
        assert tmp_controller.last_state["state"] == "collect"
        assert tmp_controller.last_state["last_updated_obj"] <= datetime.datetime.now()
        assert tmp_controller.last_state["collect"] == ["collect_1", "collect_2"]
        assert tmp_controller.last_state["pass"] == []
        assert tmp_controller.last_state["fail"] == []
        assert tmp_controller.last_state["skip"] == []

    @patch("pytest_gui_status.status_gui.utils_gui.render_template", MagicMock())
    def test_backend_state_2(self, tmpdir, redis_master):
        # load new redis port
        import pytest_gui_status.status_gui.gui_backend as gui_backend
        reload_2_3(pytest_gui_status.utils)
        reload_2_3(gui_backend)
        reload_2_3(status_plugin)

        # start Redis
        redis_master.init(tmpdir.strpath)

        # setup state
        status_plugin.Helpers.on_collectstart(tmpdir.strpath)
        status_plugin.Helpers.on_collectend(tmpdir.strpath, [])
        status_plugin.Helpers.on_test_eachstart(tmpdir.strpath)
        status_plugin.Helpers.on_test_eachend(tmpdir.strpath, [
            MockTestResult("pass_1", "passed"),
            MockTestResult("fail_1", "failed"),
            MockTestResult("pass_2", "passed"),
            MockTestResult("skip_1", "skipped"),
        ])

        # mock app_gui with path
        fake_app_gui = MagicMock()
        fake_app_gui.dir_name = tmpdir.strpath

        tmp_controller = gui_backend.Controller(fake_app_gui)
        tmp_controller.redraw()

        assert tmp_controller.last_state["dir_name"] == tmpdir.strpath
        assert tmp_controller.last_state["dir_name_topfolder"] ==\
            os.path.basename(tmpdir.strpath)
        assert tmp_controller.last_state["state"] == "runtest"
        assert tmp_controller.last_state["last_updated_obj"] <= datetime.datetime.now()
        assert tmp_controller.last_state["collect"] == []
        assert sorted(tmp_controller.last_state["pass"]) == sorted(["pass_1", "pass_2"])
        assert tmp_controller.last_state["fail"] == ["fail_1"]
        assert tmp_controller.last_state["skip"] == ["skip_1"]
