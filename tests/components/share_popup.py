from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from tests.components.component import Component


class SharePopup(Component):
    POPUP = '//div[@data-qa-modal="share-access"]'
    INPUT_NAME = './/input[contains(concat(\' \',@class,\' \'),\' InputSuggest__input--3KAzA \')]'
    ACCEPT = './/button[contains(concat(\' \',@class,\' \'),\' AddUserComponent__button--1OUUw \')]'
    CHOOSE_ACCESS_TYPE = './/div[contains(concat(\' \',@class,\' \'),\' AddUserComponent__dropdown--3K12b \')]'
    VIEW_ONLY = './/div[@data-qa-value="read_only"]'
    VIEW_AND_EDIT = './/div[@data-qa-value="read_write"]'
    ERROR = './/div[@class="index__error--37wkb index__error_fix--1pEzE"]'
    GRANTED = './/div[@data-qa-email="{}"]'
    # CLOSE_BUTTON = './/svg[@class="Dialog__close--1rKyk"]'

    def __init__(self, driver):
        self.types = {
            'view_only': self.VIEW_ONLY,
            'view_and_edit': self.VIEW_AND_EDIT
        }
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

    def is_error_exist(self):
        # don't know how to do it in other way
        try:
            self.wait(EC.presence_of_element_located((By.XPATH, self.ERROR)))
        except exceptions.TimeoutException:
            return False
        return True

    def choose_access_type(self, required_type):
        listbox = self.wait(EC.element_to_be_clickable((By.XPATH, self.CHOOSE_ACCESS_TYPE)))
        listbox.click()
        required = self.wait(EC.element_to_be_clickable((By.XPATH, self.types.get(required_type, self.VIEW_AND_EDIT))))
        required.click()

    def wait_till_added(self, name):
        self.wait(EC.presence_of_element_located((By.XPATH, self.GRANTED.format(name))))

    def close(self):
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.global_wait(EC.invisibility_of_element((By.XPATH, self.POPUP)))
