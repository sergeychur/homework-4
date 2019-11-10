from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class DataList(Component):
    DATALIST_DIV = '//div[contains(concat(\' \',@class,\' \'),\' b-collection__list_datalist \')]'
    CHECKBOX = './/div[@data-bem="b-checkbox"]'
    FOLDER = './/div[@data-id="{}"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.DATALIST_DIV)))

    def choose_first_file(self):
        checkbox = self.wait(EC.element_to_be_clickable((By.XPATH, self.CHECKBOX)))
        checkbox.click()

    def choose_folder_by_name(self, name):
        needed_checkbox = self.wait(EC.element_to_be_clickable((By.XPATH,
                                                                self.FOLDER.format(name) + self.CHECKBOX[1:])))
        needed_checkbox.click()
