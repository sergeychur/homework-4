import urlparse
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):
    BASE_URL = ''
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        self.driver.maximize_window()

    def wait(self, until, who=None, timeout=30, step=0.1):
        if who is None:
            who = self.driver
        return WebDriverWait(who, timeout, step).until(until)
