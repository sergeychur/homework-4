from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class NewFolderPopup(Component):
    POPUP = '//div[contains(concat(\' \',@class,\' \'),\' Dialog__root--2WO7u \')]'
    INPUT_NAME = './/div[@class="ui fluid focus input"]/input'
    ACCEPT = './/div[@class="CreateNewFolderDialog__button--7S1Hs"]/button'

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

    def create_new(self, name, base_url):
        self.fill_name(name)
        self.accept()
        print("wait for ", base_url + name + '/')
        self.global_wait(EC.url_matches(base_url + name + '/'))
    
    def create_new_no_wait(self, name, base_url):
        self.fill_name(name)
        self.accept()
    
    def create_new_with(self, name, base_url):
        self.fill_name(name)
        self.accept()
        print("wait for ", base_url)
        self.global_wait(EC.url_matches(base_url))
    


