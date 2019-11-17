import urlparse
from selenium.webdriver.support.ui import WebDriverWait


class Page(object):
    BASE_URL = 'https://cloud.mail.ru/home/'
    PATH = ''

    def __init__(self, driver):
        self.driver = driver

    def open(self, full=True):
        url = urlparse.urljoin(self.BASE_URL, self.PATH)
        self.driver.get(url)
        if full:
            self.driver.maximize_window()

    def move(self, path="", base="https://cloud.mail.ru/home"):
        url = base
        if len(path) > 0:
            if path[0] != '/':
                path = "/" + path
            if path[-1] != '/':
                path =  path + "/"
            url = url + path
        self.driver.get(url)

    def main_page(self):
        self.move()

    def wait(self, until, who=None, timeout=30, step=0.1):
        if who is None:
            who = self.driver
        return WebDriverWait(who, timeout, step).until(until)
