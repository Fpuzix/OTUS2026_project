import allure
import pytest


@allure.feature("API")
@allure.story("Auth")
@pytest.mark.api
class TestAuth:
    @allure.title("Basic auth succeeds with valid credentials")
    def test_basic_auth_success(self, httpbin_client):
        response = httpbin_client.get(
            "/basic-auth/user/pass", auth=("user", "pass"), expected_status=200
        )

        body = response.json()
        assert body["authenticated"] is True
        assert body["user"] == "user"

    @allure.title("Basic auth fails with invalid credentials")
    def test_basic_auth_failure(self, httpbin_client):
        response = httpbin_client.get(
            "/basic-auth/user/pass", auth=("user", "wrong"), expected_status=401
        )

        assert response.status_code == 401
