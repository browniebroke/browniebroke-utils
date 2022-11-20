from pathlib import Path

from browniebroke_utils.setup_prettier import PRETTIER_XML, XML_TO_ADD, main

BASE_WORKSPACE_XML = """<?xml version="1.0" encoding="UTF-8"?>
<project version="4">
  <component name="PropertiesComponent">
    <property name="ASKED_ADD_EXTERNAL_FILES" value="true" />
    <property name="RunOnceActivity.OpenProjectViewOnStart" value="true" />
  </component>
  <component name="TerminalProjectNonSharedOptionsProvider">
    <option name="shellPath" value="/bin/zsh" />
  </component>
</project>"""


def test_constants():
    assert (
        '<property name="prettier.files.pattern" '
        'value="{**/*,*}.{js,ts,jsx,tsx,json,md,yml,yaml}" />' in XML_TO_ADD
    )
    assert (
        '<option name="myFilesPattern" '
        'value="{**/*,*}.{js,ts,jsx,tsx,json,md,yaml,yml}" />' in PRETTIER_XML
    )


def test_main(fs):
    dot_idea = Path(".idea")
    dot_idea.mkdir()
    workspace_xml = dot_idea / "workspace.xml"
    workspace_xml.write_text(BASE_WORKSPACE_XML)

    main()

    prettier_xml = dot_idea / "prettier.xml"
    assert prettier_xml.exists()
    assert prettier_xml.read_text() == PRETTIER_XML

    workspace_xml_content = workspace_xml.read_text()
    assert (
        '<property name="prettier.files.pattern" '
        'value="{**/*,*}.{js,ts,jsx,tsx,json,md,yml,yaml}"' in workspace_xml_content
    )
