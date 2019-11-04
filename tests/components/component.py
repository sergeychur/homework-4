from selenium.webdriver.support.ui import WebDriverWait

class Component:
    def __init__(self, driver):
        self.driver = driver

    def wait(self, until):
        return WebDriverWait(self.driver, 30, 0.1).until(until)