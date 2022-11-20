from pathlib import Path

TEMPLATES_DIR = Path(__file__).parent / "templates" / "pywatchers"

WATCHER_TASKS_XML = (TEMPLATES_DIR / "watchers.xml").read_text()


def main() -> None:
    root_path = Path.cwd()
    idea_path = root_path / ".idea"
    watcher_tasks = idea_path / "watcherTasks.xml"
    watcher_tasks.write_text(WATCHER_TASKS_XML)
