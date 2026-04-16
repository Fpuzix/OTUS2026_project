from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    FIRST_NAME_INPUT = (By.ID, "first-name")
    LAST_NAME_INPUT = (By.ID, "last-name")
    POSTAL_CODE_INPUT = (By.ID, "postal-code")
    CONTINUE_BUTTON = (By.ID, "continue")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    SUMMARY_INFO = (By.CSS_SELECTOR, "[data-test='summary-info']")
    FINISH_BUTTON = (By.ID, "finish")
    COMPLETE_HEADER = (By.CSS_SELECTOR, "[data-test='complete-header']")
    BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def wait_until_information_step_open(self) -> None:
        self.wait_url_contains("checkout-step-one.html")
        self.wait_visible(self.CONTINUE_BUTTON)
        self.wait_visible(self.FIRST_NAME_INPUT)

    def is_information_step_opened(self) -> bool:
        return self.current_url_contains(
            "checkout-step-one.html"
        ) and self.is_displayed(self.CONTINUE_BUTTON)

    def get_title_text(self) -> str:
        return self.get_text(self.TITLE)

    def fill_checkout_information(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        self.wait_until_information_step_open()
        self.type(self.FIRST_NAME_INPUT, first_name)
        self.type(self.LAST_NAME_INPUT, last_name)
        self.type(self.POSTAL_CODE_INPUT, postal_code)

    def continue_checkout(
        self, first_name: str, last_name: str, postal_code: str
    ) -> None:
        self.fill_checkout_information(first_name, last_name, postal_code)
        self.click(self.CONTINUE_BUTTON)

    def get_error_message(self) -> str:
        return self.get_text(self.ERROR_MESSAGE)

    def wait_until_overview_step_open(self) -> None:
        self.wait_url_contains("checkout-step-two.html")
        self.wait_visible(self.SUMMARY_INFO)
        self.wait_visible(self.FINISH_BUTTON)

    def is_overview_step_opened(self) -> bool:
        return self.current_url_contains(
            "checkout-step-two.html"
        ) and self.is_displayed(self.FINISH_BUTTON)

    def wait_until_complete_page_open(self) -> None:
        self.wait_url_contains("checkout-complete.html")
        self.wait_visible(self.COMPLETE_HEADER)
        self.wait_visible(self.BACK_HOME_BUTTON)

    def finish_checkout(self) -> None:
        self.wait_until_overview_step_open()
        self.click(self.FINISH_BUTTON)
        self.wait_until_complete_page_open()

    def is_complete_page_opened(self) -> bool:
        return self.current_url_contains(
            "checkout-complete.html"
        ) and self.is_displayed(self.COMPLETE_HEADER)

    def get_complete_header_text(self) -> str:
        self.wait_until_complete_page_open()
        return self.get_text(self.COMPLETE_HEADER)
