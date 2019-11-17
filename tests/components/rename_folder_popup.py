from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class RenameFolderPopup(Component):
    POPUP = '//div[@class="layer_rename"]'
    INPUT_NAME = './/div[@class="layer__fieldset"]/input'
    ACCEPT = './/button[@data-name="rename"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))

    def accept(self):
        accept_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.ACCEPT)))
        accept_button.click()

    def fill_name(self, name):
        input_field = self.wait(EC.element_to_be_clickable((By.XPATH, self.INPUT_NAME)))
        input_field.clear()
        input_field.click()
        input_field.send_keys(name)

    def rename(self, name, base_url):
        self.fill_name(name)
        self.accept()
        self.global_wait(EC.url_matches(base_url + name + '/'))
    
    def rename_no_wait(self, name, base_url):
        self.fill_name(name)
        self.accept()


