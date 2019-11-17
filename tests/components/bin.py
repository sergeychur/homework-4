# coding=utf-8
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class Bin(Component):
    RESTORE_BTN = '(//span[@class="b-toolbar__btn__text b-toolbar__btn__text_pad"][contains(.,"Восстановить")])[1]'
    CLEAR_BIN_BTN = '(//div[@data-bem="b-toolbar__btn"][@data-name="clear"])[1]'
    CONFIRM_CLEAR = '//button[@data-name="empty"]'
    FILES_LISTS_ROW = '//div[@class="DataListRow__root--bZaRr"]'
    EMPTY_MSG = '//div[@class="Bin__empty--3f_KI"]'
    FOLDER_LINK = '//div[contains(@data-id,"/{}")][@class="b-nav__item js-href b-nav__item_active"]'
    RESTORE = '//button[@data-bem="btn"][contains(.,"Восстановить")]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.CLEAR_BIN_BTN)))

    def __get_items_list(self):
        self.wait(EC.presence_of_element_located((By.XPATH, self.FILES_LISTS_ROW)), 5)
        items_rows = self.driver.find_elements(By.XPATH, self.FILES_LISTS_ROW)
        return items_rows

    def get_items_names(self):
        items = self.__get_items_list()
        return [item.text.split('\n')[0] for item in items]

    def clear(self):
        clear_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CLEAR_BIN_BTN)))
        clear_btn.click()
        confirm_clear = self.wait(EC.element_to_be_clickable((By.XPATH, self.CONFIRM_CLEAR)))
        confirm_clear.click()
        self.wait(EC.presence_of_element_located((By.XPATH, self.EMPTY_MSG)))

    def is_empty(self):
        return len(self.driver.find_elements(By.XPATH, self.EMPTY_MSG)) == 0

    def restore_file(self, name, folder_name):
        file_links = self.__get_items_list()
        file_row = next((f for f in file_links if f.text.split('\n')[0] == name), None)
        file_row.click()
        restore_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.RESTORE_BTN)))
        restore_btn.click()
        folder_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.FOLDER_LINK.format(folder_name))))
        folder_link.click()
        restore_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.RESTORE)))
        restore_btn.click()
