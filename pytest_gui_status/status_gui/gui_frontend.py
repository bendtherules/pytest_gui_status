import htmlPy
import os
import sys
from PyQt4.QtGui import QApplication
import PyQt4.QtCore as QtCore

# Import back-end functionalities
from gui_backend import Controller


if len(sys.argv) > 1:
    dir_name_raw = sys.argv[1]
else:
    dir_name_raw = "."
dir_name = os.path.abspath(dir_name_raw)

# GUI initializations
app = htmlPy.AppGUI(title=u"{dir_name} - Test Status".format(dir_name=dir_name),
                    developer_mode=True, width=150, height=80)
app.window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
screen_geo = QApplication.desktop().availableGeometry()
screen_topright = screen_geo.topRight()
app.x_pos = (screen_topright.x() - 20) - app.width
app.y_pos = (screen_topright.y() + 20)
# import pdb;pdb.set_trace()

# GUI configarg
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.static_path = os.path.join(BASE_DIR, "static/")
app.template_path = os.path.join(BASE_DIR, "tmpl/")
app.dir_name = dir_name

# Register back-end functionalities
app_backend = Controller(app)
app.bind(app_backend)

# GUI render config
# app.html = u""
app_backend.redraw()


# Start application
if __name__ == "__main__":
    app.start()
