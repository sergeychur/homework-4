from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component
from tests.components.datalist import DataList

from tests.components.new_folder_popup import NewFolderPopup


class CopyFolderPopup(Component):
    POPUP = '//div[@class="layer_copy"]'
    POPUPM = '//div[@class="layer_move"]'
    #POPUP = '//div[contains(concat(\' \',@class,\' \'),\' layer_copy \')]'
    CREATE_BUTTON = './/button[@data-name="create-folder"]'
    COPY_BUTTON = './/button[@data-name="copy"]'
    MOVE_BUTTON = './/button[@data-name="move"]'
    FOLDER = './/a[@href="/home/{}/"]'

    def __init__(self, driver, copy=True):
        Component.__init__(self, driver=driver)
        if copy:
            self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))
        else:
            self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUPM)))

    def create_folder(self, name, home_url):
        create_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_BUTTON)))
        create_button.click()
        new_folder_popup = NewFolderPopup(self.driver)
        new_folder_popup.create_new_no_wait(name, home_url)

    def copy(self):
        copy_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.COPY_BUTTON)))
        copy_button.click()

    def move(self):
        copy_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.MOVE_BUTTON)))
        copy_button.click()

    def copy_to_folder(self, name, copy=True):
        needed_checkbox = self.wait(EC.element_to_be_clickable((By.XPATH, self.FOLDER.format(name))))
        needed_checkbox.click()
        if copy:
            self.copy()
        else:
            self.move()