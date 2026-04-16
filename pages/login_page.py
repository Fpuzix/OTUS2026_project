import allure
from selenium.webdriver.common.by import By

from data.test_data import STANDARD_USER, VALID_PASSWORD
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    LOGIN_LOGO = (By.CLASS_NAME, "login_logo")

    def open_page(self) -> None:
        with allure.step("Open login page"):
            self.open()
            self.wait_until_open()

    def wait_until_open(self) -> None:
        self.wait_visible(self.LOGIN_BUTTON)
        self.wait_visible(self.USERNAME_INPUT)

    def enter_username(self, username: str) -> None:
        self.type(self.USERNAME_INPUT, username)

    def enter_password(self, password: str) -> None:
        self.type(self.PASSWORD_INPUT, password)

    def click_login(self) -> None:
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        with allure.step(f"Login as {username}"):
            self.enter_username(username)
            self.enter_password(password)
            self.click_login()

    def login_as_standard_user(self) -> None:
        self.login(STANDARD_USER, VALID_PASSWORD)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def is_login_form_displayed(self) -> bool:
        return (
            self.is_displayed(self.USERNAME_INPUT)
            and self.is_displayed(self.PASSWORD_INPUT)
            and self.is_displayed(self.LOGIN_BUTTON)
        )

    def is_page_opened(self) -> bool:
        return self.is_login_form_displayed()
