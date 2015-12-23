def test_after_sessionstart(status_plugin_debug):
    debug_data = status_plugin_debug["after_sessionstart"]

    assert debug_data["collect"] == []
    assert debug_data["pass"] == []
    assert debug_data["fail"] == []
    assert debug_data["skip"] == []

    assert debug_data["state"] == "start"


def test_after_first_collectstart(status_plugin_debug):
    debug_data = status_plugin_debug["after_first_collectstart"]

    assert debug_data["collect"] == []
    assert debug_data["pass"] == []
    assert debug_data["fail"] == []
    assert debug_data["skip"] == []

    assert debug_data["state"] == "collect"


def test_after_last_itemcollected(status_plugin_debug):
    debug_data = status_plugin_debug["after_last_itemcollected"]

    # if the tests in this file change, adjust this list too
    assert debug_data["collect"] == ["test_after_sessionstart",
                                     "test_after_first_collectstart",
                                     "test_after_last_itemcollected",
                                     "test_after_first_runtest_logstart",
                                     "test_after_this_runtest_logstart"]
    assert debug_data["pass"] == []
    assert debug_data["fail"] == []
    assert debug_data["skip"] == []

    assert debug_data["state"] == "collect"


def test_after_first_runtest_logstart(status_plugin_debug):
    debug_data = status_plugin_debug["after_first_runtest_logstart"]

    assert debug_data["pass"] == []
    assert debug_data["fail"] == []
    assert debug_data["skip"] == []

    assert debug_data["state"] == "runtest"


def test_after_this_runtest_logstart(status_plugin_debug):
    debug_data = status_plugin_debug["after_this_runtest_logstart"]

    assert len(debug_data["pass"] + debug_data["fail"] + debug_data["skip"]) > 0

    assert debug_data["state"] == "runtest"
