import pytest_gui_status.status_plugin.plugin as status_plugin

from mock import patch, MagicMock
import redis
import pytest

REDIS_TEST_PORT = status_plugin.REDIS_PORT + 1

mock_htmlPy_module = MagicMock()
mock_htmlPy_module.Object = object
mock_htmlPy_module.Slot.return_value = (lambda func: func)


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
def test_redis_fail_1(tmpdir):
    # load new redis port
    import pytest_gui_status.status_gui.gui_backend as gui_backend
    reload(gui_backend)
    reload(status_plugin)

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

    assert error_info.value.message == "Cant connect to this socket. Is redis running?\n" \
        + "Stopping pytest_status_gui"


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
def test_redis_fail_2(tmpdir):
    # load new redis port
    import pytest_gui_status.status_gui.gui_backend as gui_backend
    reload(gui_backend)
    reload(status_plugin)

    # start Redis
    status_plugin.Helpers.on_start(tmpdir.strpath)

    # make PYTEST_STATUS_DB value corrupt/incorrect
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    redis_db.set("PYTEST_STATUS_DB", "0")

    # mock Controller requirements and app_gui.stop
    fake_app_gui = MagicMock()
    with pytest.raises(redis.exceptions.ConnectionError) as error_info:
        gui_backend.Controller(fake_app_gui).redraw()

    assert error_info.value.message == "Redis is running on this port, but it is not related to pytest status\n"\
        + "Stopping pytest_status_gui"

    fake_app_gui.stop.assert_called_with()

    # cleanup or in next test it cant be started there
    redis_db.shutdown()


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
def test_redis_fail_3(tmpdir):
    # load new redis port
    import pytest_gui_status.status_gui.gui_backend as gui_backend
    reload(gui_backend)
    reload(status_plugin)

    # start Redis
    status_plugin.Helpers.on_start(tmpdir.strpath)

    # delete PYTEST_STATUS_DB
    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)
    redis_db.delete("PYTEST_STATUS_DB")

    # mock Controller requirements and app_gui.stop
    fake_app_gui = MagicMock()

    with pytest.raises(redis.exceptions.ConnectionError) as error_info:
        gui_backend.Controller(fake_app_gui).redraw()

    assert error_info.value.message == "Redis is running on this port, but it is not related to pytest status\n"\
        + "Stopping pytest_status_gui"

    fake_app_gui.stop.assert_called_with()

    # cleanup or in next test it cant be started there
    redis_db.shutdown()


@patch.dict("os.environ",
            {"PYTEST_STATUS_PORT": str(REDIS_TEST_PORT)})
@patch.dict("sys.modules", {"htmlPy": mock_htmlPy_module})
def test_redis_fail_4(tmpdir):
    # load new redis port
    import pytest_gui_status.status_gui.gui_backend as gui_backend
    reload(gui_backend)
    reload(status_plugin)

    # start Redis
    status_plugin.Helpers.on_start(tmpdir.strpath)

    redis_db = redis.StrictRedis(host='localhost', port=REDIS_TEST_PORT, db=0)

    # mock Controller requirements and app_gui.stop
    # provide invalid path
    fake_app_gui = MagicMock()
    fake_app_gui.dir_name = r"Invalid/Path"

    with pytest.raises(redis.exceptions.ConnectionError) as error_info:
        gui_backend.Controller(fake_app_gui).redraw()

    assert error_info.value.message == "dir_name = {dir_name} not found in redis db".format(
        dir_name=fake_app_gui.dir_name)

    fake_app_gui.stop.assert_called_with()

    # cleanup or in next test it cant be started there
    redis_db.shutdown()
