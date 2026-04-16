import allure
import pytest

from data.test_data import PRODUCT_SLUGS


@allure.feature("UI")
@allure.story("Inventory")
@pytest.mark.ui
class TestInventory:
    @allure.title("Inventory page opens after successful login")
    def test_inventory_page_opens_after_login(self, authorized_inventory_page):
        assert authorized_inventory_page.is_page_opened()
        assert authorized_inventory_page.get_title_text() == "Products"

    @allure.title("User can add one product to cart")
    def test_add_one_product_to_cart(self, authorized_inventory_page):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])

        assert authorized_inventory_page.is_remove_button_displayed_for(
            PRODUCT_SLUGS["backpack"]
        )
        assert authorized_inventory_page.is_cart_badge_displayed()
        assert authorized_inventory_page.get_cart_badge_text() == "1"

    @allure.title("User can remove product from cart")
    def test_remove_product_from_cart(self, authorized_inventory_page):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.remove_product_from_cart(PRODUCT_SLUGS["backpack"])

        assert authorized_inventory_page.is_add_button_displayed_for(
            PRODUCT_SLUGS["backpack"]
        )
        assert not authorized_inventory_page.is_cart_badge_displayed()
