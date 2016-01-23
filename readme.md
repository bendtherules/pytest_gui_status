Pytest Status GUI
==================

| Travis CI     | Appveyor (skipped 2.x)      | Circle CI |
| ------------- | ------------- | --------- |
|  [![Travis Build][Travis_SVG_Link]][Travis_Project_Page] | [![Appveyor Build][Appveyor_SVG_Link]][Appveyor_Project_Page] | [![CircleCI Build][CircleCI_SVG_Link]][CircleCI_Project_Page] |

### => Always on GUI for showing test status (with pytest) 

![In action][demo_gif_link]

#### Install
 `pip install pytest_gui_status`

 Also, install `PySide` and `Redis` manually via apt-get or installers.

#### How to use?
`py.test --show_status_gui`

**Recommended** : Use with [pytest-watch][ptw_gh_link] using `ptw -- --show_status_gui`

pytest-watch re-runs py.test on any change to your code

#### What is it?

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

#### Configuration

##### Template:
###### Minimal Window:

//TODO

###### Use your own template:

//TODO

##### Redis:
###### Custom Redis Command:
Set ENV variable `REDIS_PATH`

###### Custom Redis Args:
Set ENV variable `REDIS_ARGS`


###### Custom Redis Port:
Set ENV variable `PYTEST_STATUS_PORT`



### Contribution

1. Todo are currently tracked in todo.txt - I will probably move over some of it to gh issues, but it is invaluable for offline usage for me. I couldn't find a good service out there that allows file-based issue tracking with gh issue sync, but I certainly hope there is one.
2. Python 3.x tests seem to have an odd problem with Appveyor - py.test exits, but the tests machine doesn't shutdown as it apparently doesn't get the exit code, so it times out and fails. Whats interesting is that I thought after moving over to Tox this problem would be gone for good, but it didnt. Because it happens only in 3.x versions of python, it is probably because of something I have written and not their own bug. Maybe the db service is still running? But in my local windows machine, it doesn't + why only in 3.x versions of python? Can you help me with it?
3. Publishing to pypi is still a local and manual process - I would like to move that over to one of the CI servers with build and push triggered by a git tag. Also, it should build to as many pip formats as possible including zip, egg, (exe for win32 and win64). Duggan/pontoon has this mechanism, can you do the same for this?


### License

WTFPL - Do What the Fuck You Want to Public License
