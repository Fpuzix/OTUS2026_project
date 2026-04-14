import allure
import pytest


@allure.feature("API")
@allure.story("Headers and request data")
@pytest.mark.api
class TestHeaders:
    @allure.title("Headers endpoint returns sent my header")
    def test_headers_endpoint_returns_custom_header(self, httpbin_client):
        response = httpbin_client.get(
            "/headers",
            headers={"X-Project-Name": "mvp-framework"},
            expected_status=200,
        )

        body = response.json()
        assert body["headers"]["X-Project-Name"] == "mvp-framework"

    @allure.title("User-Agent endpoint returns client user agent")
    def test_user_agent_endpoint_returns_client_user_agent(self, httpbin_client):
        response = httpbin_client.get("/user-agent", expected_status=200)

        payload = response.json()
        assert "qa-framework/1.0" in payload["user-agent"]

    @allure.title("Response headers endpoint returns single requested header")
    def test_response_headers_single_header(self, httpbin_client):
        response = httpbin_client.get(
            "/response-headers",
            params={"freeform": "yes"},
            expected_status=200,
        )

        assert response.headers["freeform"] == "yes"
        assert response.json()["freeform"] == "yes"

    @allure.title("Response headers endpoint returns multiple requested headers")
    def test_response_headers_multiple_headers(self, httpbin_client):
        response = httpbin_client.get(
            "/response-headers",
            params={"x-one": "1", "x-two": "2"},
            expected_status=200,
        )

        assert response.headers["x-one"] == "1"
        assert response.headers["x-two"] == "2"
        body = response.json()
        assert body["x-one"] == "1"
        assert body["x-two"] == "2"

    @allure.title("GET endpoint echoes query args")
    def test_get_endpoint_echoes_args(self, httpbin_client):
        params = {"feature": "reporting", "scope": "smoke"}
        response = httpbin_client.get("/get", params=params, expected_status=200)

        assert response.json()["args"] == params
