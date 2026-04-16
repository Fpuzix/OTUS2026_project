import allure
import pytest

from data.test_data import (
    INVALID_PASSWORD,
    LOCKED_OUT_USER,
    STANDARD_USER,
    VALID_PASSWORD,
)


@allure.feature("UI")
@allure.story("Login")
@pytest.mark.ui
class TestLogin:
    @allure.title("Successful login with valid credentials")
    def test_successful_login(self, login_page, inventory_page):
        login_page.open_page()
        login_page.login(STANDARD_USER, VALID_PASSWORD)

        assert inventory_page.is_page_opened()
        assert inventory_page.get_title_text() == "Products"

    @allure.title("Login fails with invalid password")
    def test_login_with_invalid_password(self, login_page):
        login_page.open_page()
        login_page.login(STANDARD_USER, INVALID_PASSWORD)

        assert "Username and password do not match" in login_page.get_error_message()

    @allure.title("Login fails with empty username and password")
    def test_login_with_empty_credentials(self, login_page):
        login_page.open_page()
        login_page.click_login()

        assert "Username is required" in login_page.get_error_message()

    @allure.title("Locked out user cannot login")
    def test_locked_out_user_cannot_login(self, login_page):
        login_page.open_page()
        login_page.login(LOCKED_OUT_USER, VALID_PASSWORD)

        assert "Sorry, this user has been locked out" in login_page.get_error_message()
