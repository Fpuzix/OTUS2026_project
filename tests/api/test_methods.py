import allure
import pytest


@allure.feature("API")
@allure.story("HTTP methods")
@pytest.mark.api
class TestMethods:
    @allure.title("GET anything echoes requested path")
    def test_get_anything_with_path_parameter(self, httpbin_client):
        response = httpbin_client.get("/anything/custom/path", expected_status=200)

        body = response.json()
        assert body["method"] == "GET"
        assert body["url"].endswith("/anything/custom/path")

    @allure.title("GET anything echoes query parameters")
    def test_get_anything_with_query_parameters(self, httpbin_client):
        params = {"page": "1", "sort": "asc"}
        response = httpbin_client.get("/anything", params=params, expected_status=200)

        assert response.json()["args"] == params

    @allure.title("POST anything returns JSON body")
    def test_post_anything_with_json(self, httpbin_client):
        payload = {"id": 1, "action": "create"}
        response = httpbin_client.post("/anything", json=payload, expected_status=200)

        body = response.json()
        assert body["method"] == "POST"
        assert body["json"] == payload

    @allure.title("POST anything returns form data")
    def test_post_anything_with_form_data(self, httpbin_client):
        form_data = {"username": "alex", "role": "qa"}
        response = httpbin_client.post("/anything", data=form_data, expected_status=200)

        body = response.json()
        assert body["method"] == "POST"
        assert body["form"] == form_data

    @allure.title("PUT anything returns JSON body")
    def test_put_anything_with_json(self, httpbin_client):
        payload = {"id": 1, "action": "update"}
        response = httpbin_client.put("/anything", json=payload, expected_status=200)

        body = response.json()
        assert body["method"] == "PUT"
        assert body["json"] == payload

    @allure.title("PATCH anything returns JSON body")
    def test_patch_anything_with_json(self, httpbin_client):
        payload = {"field": "name", "value": "Alex"}
        response = httpbin_client.patch("/anything", json=payload, expected_status=200)

        body = response.json()
        assert body["method"] == "PATCH"
        assert body["json"] == payload

    @allure.title("DELETE anything returns JSON body")
    def test_delete_anything_with_json(self, httpbin_client):
        payload = {"soft_delete": True}
        response = httpbin_client.delete("/anything", json=payload, expected_status=200)

        body = response.json()
        assert body["method"] == "DELETE"
        assert body["json"] == payload
