from selenium.webdriver.support.ui import WebDriverWait


class Component:
    def __init__(self, driver):
        self.driver = driver
        self.root = driver

    def wait(self, until):
        return WebDriverWait(self.root, 30, 0.1).until(until)

    def global_wait(self, until):
        return WebDriverWait(self.driver, 30, 0.1).until(until)
