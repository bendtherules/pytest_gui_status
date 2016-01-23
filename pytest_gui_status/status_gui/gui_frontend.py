import htmlPy
import os

import PyQt4.QtCore as QtCore
from PyQt4.QtGui import QApplication
import argparse

# Import back-end functionalities
from gui_backend import Controller

dict_tmpl_size = {
    "default": (150, 80),
    "minimal": (50, 50)
}


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument("--dir_name", help="root directory where py.test was executed")
    arg_parser.add_argument("--minimal", help="use minimal template", action="store_true")
    parsed_args = arg_parser.parse_args()

    dir_name_raw = parsed_args.dir_name
    if dir_name_raw is None:
        dir_name_raw = "."
    dir_name = os.path.abspath(dir_name_raw)

    if parsed_args.minimal:
        app_tmpl = "minimal"
    else:
        app_tmpl = "default"

    # GUI initializations
    app = htmlPy.AppGUI(title=u"to_be_set_later",
                        developer_mode=True, width=1, height=1)

    app.window.setWindowFlags(QtCore.Qt.WindowTitleHint)
    # app.window.setWindowFlags(app.window.windowFlags() & ~QtCore.Qt.WindowMaximizeButtonHint)
    app.window.setWindowFlags(app.window.windowFlags() | QtCore.Qt.WindowStaysOnTopHint)
    app.tmpl_name = app_tmpl

    # set correct width, height
    app.width, app.height = dict_tmpl_size.get(app.tmpl_name)
    screen_geo = QApplication.desktop().availableGeometry()
    screen_topright = screen_geo.topRight()
    app.x_pos = (screen_topright.x() - 20) - app.width
    app.y_pos = (screen_topright.y() + 20)

    # GUI configarg
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.static_path = os.path.join(BASE_DIR, "static/")
    app.template_path = os.path.join(BASE_DIR, "tmpl/")
    app.dir_name = dir_name

    # Register back-end functionalities
    # allow minimal tmpl with sys.arg
    app_backend = Controller(app)
    app.bind(app_backend)

    # GUI render config
    # app.html = u""
    app_backend.redraw()

    app.start()

# Start application
if __name__ == "__main__":
    main()
