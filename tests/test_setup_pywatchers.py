from browniebroke_utils.setup_pywatchers import WATCHER_TASKS_XML


def test_constants():
    assert '<option name="name" value="black" />' in WATCHER_TASKS_XML
    assert '<option name="name" value="isort" />' in WATCHER_TASKS_XML
    assert '<option name="name" value="pyupgrade" />' in WATCHER_TASKS_XML
