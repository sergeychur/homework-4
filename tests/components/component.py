from selenium.webdriver.support.ui import WebDriverWait


class Component:
    def __init__(self, driver):
        self.driver = driver
        self.root = driver

    def wait(self, until, timeout=10, step=0.1, who=None):
        if who is None:
            who = self.root
        return WebDriverWait(who, timeout, step).until(until)

    def global_wait(self, until):
        return WebDriverWait(self.driver, 30, 0.1).until(until)
