from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from component import Component


class ToolBars(Component):
    DELETE_BUTTON = './/div[@data-name="remove"]'
    GET_LINK_BUTTON = './/div[@data-name="publish"]'
    TOOLBAR = '//div[@id="cloud_toolbars"]'
    CREATE_NEW_FOLDER_BUTTON = './/div[@data-name="createFolder"]'
    SHARE_BUTTON = './/div[@data-name="share"]'
    DISABLED = 'disabled'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        root_elem = self.wait(EC.presence_of_element_located((By.XPATH, self.TOOLBAR)))
        self.root = root_elem

    def delete(self):
        delete_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.DELETE_BUTTON)))
        delete_button.click()

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

    def is_share_button_active(self):
        share_button = self.driver.find_element_by_xpath(self.SHARE_BUTTON)
        return share_button.get_attribute(self.DISABLED) is None

