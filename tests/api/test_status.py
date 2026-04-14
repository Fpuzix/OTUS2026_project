import allure
import pytest


@allure.feature("API")
@allure.story("Status codes")
@pytest.mark.api
class TestStatusCodes:
    @pytest.mark.parametrize("status_code", [200, 201, 202, 204, 400, 418])
    @allure.title("Status endpoint returns code {status_code}")
    def test_status_endpoint(self, httpbin_client, status_code):
        response = httpbin_client.get(
            f"/status/{status_code}", expected_status=status_code
        )

        assert response.status_code == status_code
