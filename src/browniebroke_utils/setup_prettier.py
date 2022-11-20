from pathlib import Path

import xmltodict

TEMPLATES_DIR = Path(__file__).parent / "templates" / "prettier"

XML_TO_ADD = (TEMPLATES_DIR / "to_add.xml").read_text()
PRETTIER_XML = (TEMPLATES_DIR / "prettier.xml").read_text()


def main() -> None:
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
