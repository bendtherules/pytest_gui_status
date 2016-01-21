Pytest Status GUI
==================

| Travis CI     | Appveyor (skipped 2.x)      | Circle CI |
| ------------- | ------------- | --------- |
|  [![Travis Build][Travis_SVG_Link]][Travis_Project_Page] | [![Appveyor Build][Appveyor_SVG_Link]][Appveyor_Project_Page] | [![CircleCI Build][CircleCI_SVG_Link]][CircleCI_Project_Page] |

### => Always on GUI for showing test status (with pytest) 

![In action][demo_gif_link]


 `pip install pytest_gui_status`

 Also, install `PySide` manually via apt-get or installers.

### How to use?
`py.test --show_status_gui`

**Recommended** : Use with [pytest-watch][ptw_gh_link] using `ptw -- --show_status_gui`

pytest-watch re-runs py.test on any change to your code

### What is it?

pytest_status_gui is only a pytest plugin, which 

- starts (if not running) a small always-on-top GUI (using htmlpy) and redis db on test start
- updates the db with test run status (step running currently, for eg "Collecting Tests") and some details of the steps (like no. of tests passed) as it becomes available to the plugin.
- The GUI on the other hand periodically polls data (using js timer with 1 sec interval) from the db and updates itself.

The result is that you get some nifty **test status windows that update as you keep editing files**. It is inspired from **[pytddmon][pytddmon_video_link]**, which is more minimailistic and supports only nosetests.


[Travis_SVG_Link]: https://travis-ci.org/bendtherules/pytest_gui_status.svg?branch=master
[Appveyor_SVG_Link]:https://ci.appveyor.com/api/projects/status/8u7nu85k3dkhydk4?svg=true
[CircleCI_SVG_Link]:https://circleci.com/gh/bendtherules/pytest_gui_status.svg?style=svg

[Appveyor_Project_Page]:https://ci.appveyor.com/project/bendtherules/pytest-gui-status
[CircleCI_Project_Page]:https://circleci.com/gh/bendtherules/pytest_gui_status
[Travis_Project_Page]: https://travis-ci.org/bendtherules/pytest_gui_status

[ptw_gh_link]: https://github.com/joeyespo/pytest-watch
[demo_gif_link]:http://i.imgur.com/96X8AcP.gif
[pytddmon_video_link]:http://pytddmon.org/?page_id=33

