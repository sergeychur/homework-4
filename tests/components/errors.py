from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException,StaleElementReferenceException

from component import Component


class Errors(Component):
    ERROR404 = './/div[@class="http-error http-error_404"]'
    ERROR_FIELD = './/div[@class="http-error__code__text"]'
    ROOT = '//div[@id="http-error"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        root_elem = self.wait(EC.presence_of_element_located((By.XPATH, self.ROOT)))
        self.root = root_elem

    def isError404(self):
        timeout = 30
        print("here")
        try:
            self.wait(EC.presence_of_element_located((By.XPATH, self.ERROR404)), timeout)
        except TimeoutException:
            return False
        return True