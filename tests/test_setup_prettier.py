from browniebroke_utils.setup_prettier import PRETTIER_XML, XML_TO_ADD


def test_constants():
    assert (
        '<property name="prettier.files.pattern" '
        'value="{**/*,*}.{js,ts,jsx,tsx,json,md,yml,yaml}" />' in XML_TO_ADD
    )
    assert (
        '<option name="myFilesPattern" '
        'value="{**/*,*}.{js,ts,jsx,tsx,json,md,yaml,yml}" />' in PRETTIER_XML
    )
