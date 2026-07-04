from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    def __init__(self, driver, timeout: int = 10):
        self.driver = driver
        self.timeout = timeout
        self.wait = WebDriverWait(driver, timeout=timeout)

    BASE_URL = 'http://127.0.0.1:8010'
    PATH = None

    def open(self) -> WebElement:
        return self.driver.get(self.BASE_URL + self.PATH)


    def wait_until_visible(self, path: str) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located((By.XPATH, path)))

    def wait_until_invisible(self, path: str) -> WebElement:
        return self.wait.until(EC.invisibility_of_element_located((By.XPATH, path)))

    def wait_until_clickable(self, path: str) -> WebElement:
        return self.wait.until(EC.element_to_be_clickable((By.XPATH, path)))

    def wait_until_url_contains(self, path: str) -> bool:
        return self.wait.until(EC.url_contains(path))

    def find_element(self, path: str) -> WebElement:
        return self.driver.find_element(By.XPATH, path)

    def click_element(self, element: WebElement | str) -> None:
        if isinstance(element, str):
            self.wait_until_clickable(element).click()
        else:
            element.click()

    def input_value(self, path: str, value: str) -> None:
        self.wait_until_clickable(path).send_keys(value)

    def get_text(self, path: str) -> str:
        return self.wait_until_visible(path).text

    def clear_field(self, path: str) -> None:
        self.wait_until_clickable(path).clear()

    def accept_alert(self) -> None:
        self.wait.until(EC.alert_is_present()).accept()

    def dismiss_alert(self) -> None:
        self.wait.until(EC.alert_is_present()).dismiss()



