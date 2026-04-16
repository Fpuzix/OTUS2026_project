import allure
import pytest

from data.test_data import CHECKOUT_DATA, PRODUCT_SLUGS


@allure.feature("UI")
@allure.story("Checkout")
@pytest.mark.ui
class TestCheckout:
    @allure.title("User can proceed to checkout overview with valid data")
    def test_checkout_overview_opens_with_valid_data(
        self, authorized_inventory_page, cart_page, checkout_page
    ):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.open_cart()

        assert cart_page.is_page_opened()
        cart_page.click_checkout()

        assert checkout_page.is_information_step_opened()
        assert checkout_page.get_title_text() == "Checkout: Your Information"

        checkout_page.continue_checkout(**CHECKOUT_DATA)

        assert checkout_page.is_overview_step_opened()
        assert checkout_page.get_title_text() == "Checkout: Overview"

    @allure.title("User sees validation error when first name is empty")
    def test_checkout_validation_empty_first_name(
        self, authorized_inventory_page, cart_page, checkout_page
    ):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.open_cart()
        cart_page.click_checkout()

        checkout_page.continue_checkout(
            "", CHECKOUT_DATA["last_name"], CHECKOUT_DATA["postal_code"]
        )

        assert "First Name is required" in checkout_page.get_error_message()

    @allure.title("User sees validation error when last name is empty")
    def test_checkout_validation_empty_last_name(
        self, authorized_inventory_page, cart_page, checkout_page
    ):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.open_cart()
        cart_page.click_checkout()

        checkout_page.continue_checkout(
            CHECKOUT_DATA["first_name"], "", CHECKOUT_DATA["postal_code"]
        )

        assert "Last Name is required" in checkout_page.get_error_message()

    @allure.title("User sees validation error when postal code is empty")
    def test_checkout_validation_empty_postal_code(
        self, authorized_inventory_page, cart_page, checkout_page
    ):
        authorized_inventory_page.add_product_to_cart(PRODUCT_SLUGS["backpack"])
        authorized_inventory_page.open_cart()
        cart_page.click_checkout()

        checkout_page.continue_checkout(
            CHECKOUT_DATA["first_name"], CHECKOUT_DATA["last_name"], ""
        )

        assert "Postal Code is required" in checkout_page.get_error_message()
