Pytest Status GUI
==================

### Always on GUI for showing test status (only works with pytest)

`pip install pytest_gui_status`

### How to use?
`py.test --show_status_gui`

### What is it?

pytest_status_gui is only a pytest plugin, which 

- starts (if not running) a small always-on-top GUI (using htmlpy) and redis db on test start
- updates the db with test run status (step running currently, for eg "Collecting Tests") and some details of the steps (like no. of tests passed) as it becomes available to the plugin.
- The GUI on the other hand periodically polls data (using js timer with 1 sec interval) from the db and updates itself.

It is **recommended for use with pytest-watch** which re-runs pytest for every change to your code. Run like `ptw -- --show_status_gui`

The result is that you get some nifty **test status windows that update as you keep editing files**. It is inspired from **[pytddmon](http://pytddmon.org/?page_id=33)**.

