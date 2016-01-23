import htmlPy
from .utils_gui import render_template
import os
import redis
import dateutil.parser
from datetime import datetime
import humanfriendly
import os.path
from ..utils import s
from ..utils import REDIS_PORT


class Controller(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    dict_state_desc = {
        "start": "Starting Tests",
        "collect": "Collecting Tests",
        "runtest": "Running Tests",
        "end": "Finished Tests"
    }

    dict_tmpl = {
        "default": "index.html",
        "minimal": "minimal.html",
    }

    dict_tmpl_size = {
        "default": (150, 80),
        "minimal": (50, 50)
    }

    def __init__(self, app_gui):
        super(Controller, self).__init__()
        self.i = 0
        self.app_gui = app_gui
        self.last_state = None

        self.tmpl_name_full = self.dict_tmpl.get(self.app_gui.tmpl_name)
        if self.tmpl_name_full is None:
            raise TypeError("template name must be valid, one of these: {allowed_tmpl_names}".format(
                allowed_tmpl_names=(", ".join(self.dict_tmpl.keys()))))

        # set correct width, height
        # self.app_gui.window.minimumWidth, self.app_gui.window.minimumHeight = (0, 0)
        self.app_gui.width, self.app_gui.height = self.dict_tmpl_size.get(self.app_gui.tmpl_name)

        screen_geo = QApplication.desktop().availableGeometry()
        screen_topright = screen_geo.topRight()
        self.app_gui.x_pos = (screen_topright.x() - 20) - self.app_gui.width
        self.app_gui.y_pos = (screen_topright.y() + 20)

    @htmlPy.Slot()
    def redraw(self):
        redis_db = redis.StrictRedis(host='localhost', port=REDIS_PORT, db=0)
        try:
            assert redis_db.ping()
        except redis.exceptions.ConnectionError:
            self.app_gui.stop()
            raise redis.exceptions.ConnectionError("Cant connect to this socket. Is redis running?\n"
                                                   "Stopping pytest_status_gui")
        except AssertionError:
            self.app_gui.stop()
            raise redis.exceptions.ConnectionError("Cant connect to redis, something else seems to be running on this socket. "
                                                   "Is redis running?\n"
                                                   "Stopping pytest_status_gui")

        try:
            # make sure that this is correct redis db
            assert s(redis_db.get("PYTEST_STATUS_DB")) == "1"
        except AssertionError:
            self.app_gui.stop()
            raise redis.exceptions.ConnectionError("Redis is running on this port, but it is not related to pytest status\n"
                                                   "Stopping pytest_status_gui")

        dir_name = self.app_gui.dir_name
        hash_dir_name = s(redis_db.hget("directories_to_hash", dir_name))

        if hash_dir_name is None:
            self.app_gui.stop()
            raise redis.exceptions.ConnectionError("dir_name = {dir_name} not found in redis db".format(
                dir_name=dir_name))

        dict_state = {}
        dict_state["dir_name"] = dir_name
        dict_state["dir_name_topfolder"] = os.path.basename(dir_name)

        dict_state["state"] = s(redis_db.get("{hash_a}_state".format(hash_a=hash_dir_name)))
        dict_state["state_desc"] = self.dict_state_desc[dict_state["state"]]
        dict_state["last_updated"] = s(redis_db.get("{hash_a}_last_updated".format(hash_a=hash_dir_name)))

        dict_state["last_updated_obj"] = dateutil.parser.parse(dict_state["last_updated"])
        last_updated_rel = (datetime.now() - dict_state["last_updated_obj"]).seconds  # in seconds
        if last_updated_rel > 60:
            # when >1 min, reolve only upto min
            last_updated_rel = last_updated_rel - (last_updated_rel % 60)
        dict_state["last_updated_friendly"] = humanfriendly.format_timespan(last_updated_rel)

        dict_state["collect"] = s(redis_db.lrange("{hash_a}_collect".format(hash_a=hash_dir_name), 0, -1))
        dict_state["pass"] = s(redis_db.lrange("{hash_a}_pass".format(hash_a=hash_dir_name), 0, -1))
        dict_state["fail"] = s(redis_db.lrange("{hash_a}_fail".format(hash_a=hash_dir_name), 0, -1))
        dict_state["skip"] = s(redis_db.lrange("{hash_a}_skip".format(hash_a=hash_dir_name), 0, -1))

        if (not self.last_state) or (self.last_state != dict_state):
            self.app_gui.title = u"{dir_name_topfolder} - Test Status".format(
                dir_name_topfolder=dict_state["dir_name_topfolder"])
            self.app_gui.html = render_template(self.app_gui, self.tmpl_name_full, dict_state)

        self.last_state = dict_state
