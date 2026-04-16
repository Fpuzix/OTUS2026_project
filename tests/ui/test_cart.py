import allure
import pytest

from data.test_data import PRODUCT_NAMES, PRODUCT_SLUGS


@allure.feature("UI")
@allure.story("Cart")
@pytest.mark.ui
class TestCart:
    @allure.title("Added item is displayed in cart")
    def test_added_item_is_displayed_in_cart(
        self, authorized_inventory_page, cart_page
    ):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.open_cart()

        assert cart_page.is_page_opened()
        assert cart_page.get_title_text() == "Your Cart"
        assert PRODUCT_NAMES["backpack"] in cart_page.get_item_names()

    @allure.title("Cart contains all selected products")
    def test_cart_contains_selected_items(self, authorized_inventory_page, cart_page):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["bike_light"])
        authorized_inventory_page.open_cart()

        item_names = cart_page.get_item_names()

        assert PRODUCT_NAMES["backpack"] in item_names
        assert PRODUCT_NAMES["bike_light"] in item_names
        assert len(item_names) == 2
