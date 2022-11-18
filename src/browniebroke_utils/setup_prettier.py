import sys
from pathlib import Path

import xmltodict

XML_TO_ADD = """<?xml version="1.0" encoding="UTF-8"?>
<component>
  <property name="prettier.files.pattern" value="{**/*,*}.{js,ts,jsx,tsx,json,md,yml,yaml}" />
  <property name="prettierjs.PrettierConfiguration.Package" value="$USER_HOME$/.nvm/versions/node/v12.19.0/lib/node_modules/prettier" />
  <property name="run.prettier.on.save" value="true" />
  <property name="settings.editor.selected.configurable" value="settings.javascript.prettier" />
</component>
"""

PRETTIER_XML = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="PrettierConfiguration">
    <option name="myRunOnSave" value="true" />
    <option name="myFilesPattern" value="{**/*,*}.{js,ts,jsx,tsx,json,md,yaml,yml}" />
  </component>
</project>
"""

EXAMPLE_WORKSPACE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="ChangeListManager">
    <list default="true" id="d64979e0-13fb-4789-9268-966c79b5821e" name="Default Changelist" comment="" />
    <option name="SHOW_DIALOG" value="false" />
    <option name="HIGHLIGHT_CONFLICTS" value="true" />
    <option name="HIGHLIGHT_NON_ACTIVE_CHANGELIST" value="false" />
    <option name="LAST_RESOLUTION" value="IGNORE" />
  </component>
  <component name="PropertiesComponent">
    <property name="ASKED_ADD_EXTERNAL_FILES" value="true" />
    <property name="RunOnceActivity.OpenProjectViewOnStart" value="true" />
    <property name="WebServerToolWindowFactoryState" value="false" />
  </component>
  <component name="TerminalProjectNonSharedOptionsProvider">
    <option name="shellPath" value="/bin/zsh" />
  </component>
  <component name="TypeScriptGeneratedFilesManager">
    <option name="version" value="3" />
  </component>
</project>
"""


def main() -> None:
    if len(sys.argv) == 2:
        root_path = Path(sys.argv[1])
    else:
        root_path = Path.cwd()

    idea_path = root_path / ".idea"
    workspace_path = idea_path / "workspace.xml"
    workspace_xml = workspace_path.read_text()
    workspace_xml = update_workspace_xml(workspace_xml)
    workspace_path.write_text(workspace_xml)

    prettier_path = idea_path / "prettier.xml"
    prettier_path.write_text(PRETTIER_XML)


def update_workspace_xml(workspace_xml: str) -> str:
    workspace_dict = xmltodict.parse(workspace_xml)
    needed = xmltodict.parse(XML_TO_ADD)["component"]["property"]
    for component in workspace_dict["project"]["component"]:
        if component["@name"] == "PropertiesComponent":
            properties = component["property"]
            to_add = [prop for prop in needed if prop not in properties]
            properties.extend(to_add)
    return xmltodict.unparse(workspace_dict, pretty=True)


if __name__ == "__main__":
    main()
