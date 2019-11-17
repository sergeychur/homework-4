from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from component import Component
from selenium.webdriver.common.action_chains import ActionChains


class Errors(Component):
    ERROR404 = './/div[@class="http-error http-error_404"]'
    ERROR_FIELD = './/div[@class="http-error__code__text"]'
    ROOT = '//div[@id="http-error"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        root_elem = self.wait(EC.presence_of_element_located((By.XPATH, self.ROOT)))
        self.root = root_elem

    def isError404(self):
        self.wait(EC.presence_of_element_located((By.XPATH, self.ERROR404)))
        return True

    def get_link(self):
        get_link_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.GET_LINK_BUTTON)))
        if get_link_button.is_enabled():
            get_link_button.click()
        else:
            raise ElementNotInteractableException(msg='Button is disabled')

    def create_new_folder(self):
        create_new_folder_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_NEW_FOLDER_BUTTON)))
        create_new_folder_button.click()

    def share(self):
        share_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.SHARE_BUTTON)))
        share_button.click()

    def dragAndDrop(self):
        element = driver.find_element_by_name("source")
        target =  driver.find_element_by_name("target")
        ActionChains(driver).drag_and_drop(element, target).perform()

