import sys
from pathlib import Path

WATCHER_TASKS_XML = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ProjectTasksOptions">
    <TaskOptions isEnabled="true">
      <option name="arguments" value="run black $FilePath$" />
      <option name="checkSyntaxErrors" value="true" />
      <option name="description" />
      <option name="exitCodeBehavior" value="ERROR" />
      <option name="fileExtension" value="py" />
      <option name="immediateSync" value="false" />
      <option name="name" value="black" />
      <option name="output" value="" />
      <option name="outputFilters">
        <array />
      </option>
      <option name="outputFromStdout" value="false" />
      <option name="program" value="poetry" />
      <option name="runOnExternalChanges" value="false" />
      <option name="scopeName" value="Project Files" />
      <option name="trackOnlyRoot" value="false" />
      <option name="workingDir" value="$ProjectFileDir$" />
      <envs />
    </TaskOptions>
    <TaskOptions isEnabled="true">
      <option name="arguments" value="run isort $FilePath$" />
      <option name="checkSyntaxErrors" value="true" />
      <option name="description" />
      <option name="exitCodeBehavior" value="ERROR" />
      <option name="fileExtension" value="py" />
      <option name="immediateSync" value="false" />
      <option name="name" value="isort" />
      <option name="output" value="" />
      <option name="outputFilters">
        <array />
      </option>
      <option name="outputFromStdout" value="false" />
      <option name="program" value="poetry" />
      <option name="runOnExternalChanges" value="false" />
      <option name="scopeName" value="Project Files" />
      <option name="trackOnlyRoot" value="false" />
      <option name="workingDir" value="$ProjectFileDir$" />
      <envs />
    </TaskOptions>
    <TaskOptions isEnabled="true">
      <option name="arguments" value="run pyupgrade --py36-plus $FilePath$" />
      <option name="checkSyntaxErrors" value="true" />
      <option name="description" />
      <option name="exitCodeBehavior" value="NEVER" />
      <option name="fileExtension" value="py" />
      <option name="immediateSync" value="false" />
      <option name="name" value="pyupgrade" />
      <option name="output" value="" />
      <option name="outputFilters">
        <array />
      </option>
      <option name="outputFromStdout" value="false" />
      <option name="program" value="poetry" />
      <option name="runOnExternalChanges" value="false" />
      <option name="scopeName" value="Project Files" />
      <option name="trackOnlyRoot" value="false" />
      <option name="workingDir" value="$ProjectFileDir$" />
      <envs />
    </TaskOptions>
  </component>
</project>
"""


def main() -> None:
    if len(sys.argv) == 2:
        root_path = Path(sys.argv[1])
    else:
        root_path = Path.cwd()
    idea_path = root_path / ".idea"
    watcher_tasks = idea_path / "watcherTasks.xml"
    watcher_tasks.write_text(WATCHER_TASKS_XML)


if __name__ == "__main__":
    main()
