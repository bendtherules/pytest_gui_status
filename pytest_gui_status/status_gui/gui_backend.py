import htmlPy
from utils import render_template
import os
import redis
import dateutil.parser
from datetime import datetime
import humanfriendly
import os.path


env_redis_port = os.environ.get("pytest_status_port")
if env_redis_port:
    REDIS_PORT = int(env_redis_port)
else:
    REDIS_PORT = 5946


class Controller(htmlPy.Object):
    # GUI callable functions have to be inside a class.
    # The class should be inherited from htmlPy.Object.
    dict_state_desc = {
        "start": "Starting Tests",
        "collect": "Collecting Tests",
        "runtest": "Running Tests",
        "end": "Finished Tests"
    }

    def __init__(self, app_gui):
        super(Controller, self).__init__()
        self.i = 0
        self.app_gui = app_gui
        self.last_state = None
        # Initialize the class here, if required.

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
            assert redis_db.get("PYTEST_STATUS_DB") == "1"
        except AssertionError:
            self.app_gui.stop()
            raise redis.exceptions.ConnectionError("Redis is running on this port, but it is not related to pytest status\n"
                                                   "Stopping pytest_status_gui")

        dir_name = self.app_gui.dir_name
        hash_dir_name = redis_db.hget("directories_to_hash", dir_name)

        if hash_dir_name is None:
            raise Exception("dir_name = {dir_name} not found in redis db".format(
                dir_name=dir_name))

        dict_state = {}
        dict_state["dir_name"] = dir_name
        dict_state["dir_name_topfolder"] = os.path.basename(dir_name)

        dict_state["state"] = redis_db.get("{hash_a}_state".format(hash_a=hash_dir_name))
        dict_state["state_desc"] = self.dict_state_desc[dict_state["state"]]
        dict_state["last_updated"] = redis_db.get("{hash_a}_last_updated".format(hash_a=hash_dir_name))

        dict_state["last_updated_obj"] = dateutil.parser.parse(dict_state["last_updated"])
        last_updated_rel = (datetime.now() - dict_state["last_updated_obj"]).seconds  # in seconds
        if last_updated_rel > 60:
            # when >1 min, reolve only upto min
            last_updated_rel = last_updated_rel - (last_updated_rel % 60)
        dict_state["last_updated_friendly"] = humanfriendly.format_timespan(last_updated_rel)

        dict_state["collect"] = redis_db.lrange("{hash_a}_collect".format(hash_a=hash_dir_name), 0, -1)
        dict_state["pass"] = redis_db.lrange("{hash_a}_pass".format(hash_a=hash_dir_name), 0, -1)
        dict_state["fail"] = redis_db.lrange("{hash_a}_fail".format(hash_a=hash_dir_name), 0, -1)
        dict_state["skip"] = redis_db.lrange("{hash_a}_skip".format(hash_a=hash_dir_name), 0, -1)

        if (not self.last_state) or (self.last_state != dict_state):
            self.app_gui.html = render_template(self.app_gui, "index.html", dict_state)

        self.last_state = dict_state
