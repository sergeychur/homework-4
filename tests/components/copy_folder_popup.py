from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component
from tests.components.datalist import DataList

from tests.components.new_folder_popup import NewFolderPopup


class CopyFolderPopup(Component):
    POPUP = '//div[@class="layer_copy"]'
    #POPUP = '//div[contains(concat(\' \',@class,\' \'),\' layer_copy \')]'
    CREATE_BUTTON = './/button[@data-name="create-folder"]'
    COPY_BUTTON = './/button[@data-name="copy"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))

    def create_folder(self, name, home_url):
        create_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_BUTTON)))
        create_button.click()
        new_folder_popup = NewFolderPopup(self.driver)
        new_folder_popup.create_new_no_wait(name, home_url)

    def copy(self):
        copy_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.COPY_BUTTON)))
        copy_button.click()

    def copy_to_folder(self, name):
        self.datalist = DataList(self.driver)
        self.datalist.choose_by_name(name)
        self.copy()