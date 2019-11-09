from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class GetLinkPopup(Component):
    LINK_INPUT = './/input[@class="PublishNew__input--1P0Zg"]'
    POPUP = '//div[@data-qa-modal="publish"]'
    LINK_VALUE = 'value'
    CLOSE_ACCESS = './/div[@class="PublishNew__controls--1cTlD"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))

    def get_link_value(self):
        link_input = self.wait(EC.presence_of_element_located((By.XPATH, self.LINK_INPUT)))
        return link_input.get_attribute(self.LINK_VALUE)

    def close_access(self):
        close_button = self.wait(EC.presence_of_element_located((By.XPATH, self.CLOSE_ACCESS)))
        close_button.click()

    def close_popup(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.global_wait(EC.invisibility_of_element((By.XPATH, self.POPUP)))

