from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from tests.components.component import Component


class DataList(Component):
    DATALIST_DIV = '//div[contains(concat(\' \',@class,\' \'),\' b-collection__list_datalist \')]'
    FILE_ICON = '//div[@data-id="{}"][@data-bem="b-thumb"]'
    CHECKBOX = './/div[@data-bem="b-checkbox"]'
    FOLDER = './/div[@data-id="{}"]'
    FILES_NAMES = '//div[@class="b-filename__text"]'

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

    def does_file_exist(self, path):
        try:
            self.wait(EC.element_to_be_clickable((By.XPATH, self.FILE_ICON.format(path))))
            return True
        except TimeoutException:
            return False

    def get_files_names_list(self):
        files_number = len(self.driver.find_elements(By.XPATH, self.FILES_NAMES))
        result = []
        for i in range(1, files_number + 1):
            file_name = self.wait(EC.presence_of_element_located(
                (By.XPATH, '({})[{}]'.format(self.FILES_NAMES, i)))).text
            result.append(file_name)
        return result
