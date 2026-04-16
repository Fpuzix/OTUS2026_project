from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class BasePage:
    def __init__(self, driver: WebDriver, base_url: str, timeout: int = 10):
        self.driver = driver
        self.base_url = base_url
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout)

    def open(self, path: str = "") -> None:
        self.driver.get(f"{self.base_url}{path.lstrip('/')}")

    def wait_visible(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def wait_clickable(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable(locator))

    def wait_presence(self, locator: tuple[str, str]) -> WebElement:
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_url_contains(self, value: str) -> bool:
        return self.wait.until(EC.url_contains(value))

    def current_url_contains(self, value: str) -> bool:
        return value in self.driver.current_url

    def click(self, locator: tuple[str, str]) -> None:
        self.wait_clickable(locator).click()

    def type(self, locator: tuple[str, str], text: str, clear: bool = True) -> None:
        element = self.wait_visible(locator)
        if clear:
            element.clear()
        element.send_keys(text)

    def get_text(self, locator: tuple[str, str]) -> str:
        return self.wait_visible(locator).text

    def is_displayed(self, locator: tuple[str, str]) -> bool:
        try:
            return self.wait_visible(locator).is_displayed()
        except TimeoutException:
            return False
