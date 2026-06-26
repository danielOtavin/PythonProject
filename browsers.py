from selenium import webdriver
from selenium.webdriver.ie.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


class ChromeManager:
    def get_driver(self):
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)


class FirefoxManager:
    def get_driver(self):
        service = Service(GeckoDriverManager().install())
        return webdriver.Firefox(service=service)


class EdgeManager:
    def get_driver(self):
        service = Service(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service)
