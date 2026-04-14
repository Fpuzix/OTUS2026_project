import xml.etree.ElementTree as ET

import allure
import pytest


@allure.feature("API")
@allure.story("XML")
@pytest.mark.api
class TestXml:
    @allure.title("XML endpoint returns slideshow root element")
    def test_xml_root_element(self, httpbin_client):
        response = httpbin_client.get("/xml", expected_status=200)

        root = ET.fromstring(response.text)

        assert root.tag == "slideshow"
        assert root.attrib["title"] == "Sample Slide Show"
        assert root.attrib["author"] == "Yours Truly"
