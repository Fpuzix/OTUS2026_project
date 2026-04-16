from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    CART_LIST = (By.CSS_SELECTOR, "[data-test='cart-list']")
    CHECKOUT_BUTTON = (By.ID, "checkout")

    def wait_until_open(self) -> None:
        self.wait_url_contains("cart.html")
        self.wait_visible(self.CART_LIST)

    def is_page_opened(self) -> bool:
        return self.current_url_contains("cart.html") and self.is_displayed(
            self.CART_LIST
        )

    def get_title_text(self) -> str:
        return self.get_text(self.TITLE)

    def get_item_names(self) -> list[str]:
        self.wait_until_open()
        elements = self.driver.find_elements(
            By.CSS_SELECTOR, "[data-test='inventory-item-name']"
        )
        return [element.text.strip() for element in elements]

    def click_checkout(self) -> None:
        self.wait_until_open()
        self.click(self.CHECKOUT_BUTTON)
