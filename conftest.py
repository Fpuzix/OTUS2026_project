import shutil
import tempfile
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from api.httpbin_client import HttpBinClient
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption(
        "--headless",
        action="store_true",
        default=False,
        help="Run browser in headless mode",
    )
    parser.addoption(
        "--base-ui-url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Base URL for UI tests",
    )
    parser.addoption(
        "--base-api-url",
        action="store",
        default="https://httpbin.org",
        help="Base URL for API tests",
    )


@pytest.fixture(scope="session")
def base_ui_url(request) -> str:
    return request.config.getoption("--base-ui-url").rstrip("/") + "/"


@pytest.fixture(scope="session")
def base_api_url(request) -> str:
    return request.config.getoption("--base-api-url").rstrip("/")


@pytest.fixture(scope="session")
def is_headless(request) -> bool:
    return request.config.getoption("--headless")


@pytest.fixture(scope="session")
def httpbin_client(base_api_url: str) -> HttpBinClient:
    return HttpBinClient(base_api_url)


@pytest.fixture
def driver(is_headless: bool):
    options = Options()
    temp_profile = tempfile.mkdtemp(prefix="otus_project_")

    prefs = {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False,
        "profile.password_manager_leak_detection": False,
        "autofill.profile_enabled": False,
        "autofill.credit_card_enabled": False,
    }

    options.add_experimental_option("prefs", prefs)
    options.add_argument(f"--user-data-dir={temp_profile}")
    options.add_argument("--disable-save-password-bubble")
    options.add_argument("--disable-notifications")
    options.add_argument(
        "--disable-features=PasswordLeakDetection,PasswordCheck,PasswordManagerOnboarding"
    )
    options.add_argument("--no-first-run")
    options.add_argument("--no-default-browser-check")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    if is_headless:
        options.add_argument("--headless=new")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(20)

    if not is_headless:
        browser.maximize_window()

    try:
        yield browser
    finally:
        browser.quit()
        shutil.rmtree(temp_profile, ignore_errors=True)


@pytest.fixture
def login_page(driver, base_ui_url) -> LoginPage:
    return LoginPage(driver, base_ui_url)


@pytest.fixture
def inventory_page(driver, base_ui_url) -> InventoryPage:
    return InventoryPage(driver, base_ui_url)


@pytest.fixture
def cart_page(driver, base_ui_url) -> CartPage:
    return CartPage(driver, base_ui_url)


@pytest.fixture
def checkout_page(driver, base_ui_url) -> CheckoutPage:
    return CheckoutPage(driver, base_ui_url)


@pytest.fixture
def authorized_inventory_page(
    login_page: LoginPage,
    inventory_page: InventoryPage,
) -> InventoryPage:
    login_page.open_page()
    login_page.login_as_standard_user()
    inventory_page.wait_until_open()
    return inventory_page


def _safe_artifact_name(nodeid: str) -> str:
    return (
        nodeid.replace("::", "__")
        .replace("/", "_")
        .replace("\\", "_")
        .replace(" ", "_")
        .replace(":", "_")
    )


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or report.passed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    test_name = _safe_artifact_name(item.nodeid)
    screenshot_path = artifacts_dir / f"{test_name}.png"

    try:
        browser.save_screenshot(str(screenshot_path))
        allure.attach.file(
            str(screenshot_path),
            name="screenshot",
            attachment_type=allure.attachment_type.PNG,
        )
    except Exception as exc:
        allure.attach(
            str(exc),
            name="screenshot_error",
            attachment_type=allure.attachment_type.TEXT,
        )

    try:
        allure.attach(
            browser.current_url,
            name="current_url",
            attachment_type=allure.attachment_type.TEXT,
        )
    except Exception as exc:
        allure.attach(
            str(exc),
            name="current_url_error",
            attachment_type=allure.attachment_type.TEXT,
        )

    try:
        allure.attach(
            browser.page_source,
            name="page_source",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as exc:
        allure.attach(
            str(exc),
            name="page_source_error",
            attachment_type=allure.attachment_type.TEXT,
        )
