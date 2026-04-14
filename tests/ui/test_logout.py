import allure
import pytest


@allure.feature("UI")
@allure.story("Logout")
@pytest.mark.ui
class TestLogout:
    @allure.title("Logout successfully")
    def test_successful_logout(self, authorized_inventory_page, login_page):
        assert authorized_inventory_page.is_page_opened()

        authorized_inventory_page.logout()
        login_page.wait_until_open()

        assert login_page.is_login_form_displayed()
