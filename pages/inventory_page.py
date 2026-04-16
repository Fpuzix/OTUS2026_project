import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "[data-test='title']")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")
    CART_BADGE = (By.CSS_SELECTOR, "[data-test='shopping-cart-badge']")
    CART_LINK = (By.CSS_SELECTOR, "[data-test='shopping-cart-link']")
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def wait_until_open(self) -> None:
        self.wait_url_contains("inventory.html")
        self.wait_visible(self.INVENTORY_CONTAINER)

    def is_page_opened(self) -> bool:
        return self.current_url_contains("inventory.html") and self.is_displayed(
            self.INVENTORY_CONTAINER
        )

    def get_title_text(self) -> str:
        return self.get_text(self.TITLE)

    def _add_button(self, product_slug: str) -> tuple[str, str]:
        return By.ID, f"add-to-cart-{product_slug}"

    def _remove_button(self, product_slug: str) -> tuple[str, str]:
        return By.ID, f"remove-{product_slug}"

    def add_product_to_cart(self, product_slug: str) -> None:
        with allure.step(f"Add product to cart: {product_slug}"):
            self.click(self._add_button(product_slug))

    def remove_product_from_cart(self, product_slug: str) -> None:
        with allure.step(f"Remove product from cart: {product_slug}"):
            self.click(self._remove_button(product_slug))

    def is_remove_button_displayed_for(self, product_slug: str) -> bool:
        return self.is_displayed(self._remove_button(product_slug))

    def is_add_button_displayed_for(self, product_slug: str) -> bool:
        return self.is_displayed(self._add_button(product_slug))

    def get_cart_badge_text(self) -> str:
        return self.get_text(self.CART_BADGE)

    def is_cart_badge_displayed(self) -> bool:
        return self.is_displayed(self.CART_BADGE)

    def open_cart(self) -> None:
        with allure.step("Open cart"):
            self.click(self.CART_LINK)

    def logout(self) -> None:
        with allure.step("Logout from inventory page"):
            self.click(self.BURGER_MENU_BUTTON)
            self.wait_visible(self.LOGOUT_LINK)
            self.click(self.LOGOUT_LINK)
