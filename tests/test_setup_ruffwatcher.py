from pathlib import Path

from browniebroke_utils.setup_ruffwatcher import WATCHER_TASKS_XML, main


def test_constants():
    assert '<option name="name" value="ruff format" />' in WATCHER_TASKS_XML
    assert '<option name="name" value="black" />' not in WATCHER_TASKS_XML
    assert '<option name="name" value="isort" />' not in WATCHER_TASKS_XML
    assert '<option name="name" value="pyupgrade" />' not in WATCHER_TASKS_XML


def test_main(fs):
    dot_idea = Path(".idea")
    dot_idea.mkdir()
    main()
    watcher_tasks_file = dot_idea / "watcherTasks.xml"
    assert watcher_tasks_file.exists()
    assert watcher_tasks_file.read_text() == WATCHER_TASKS_XML
