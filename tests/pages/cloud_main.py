# coding=utf-8

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base_page import Page
from tests.components.start_ad import StartAd


class CloudMain(Page):
    BASE_URL = 'https://cloud.mail.ru/'
    CREATE_FOLDER = '//div[@data-name="createFolder"]'

    NAME_INPUT = '//input[@value="Новая папка"]'
    NEW_NAME_INPUT = '//input[contains(@class,"layer__input")]'

    CREATE_BTN = '//button[@class="ui fluid primary button"][contains(.,"Создать")]'
    MOVE_BTN = '//button[@data-bem="btn"][contains(.,"Переместить")]'
    REMOVE_BTN = '//button[@data-bem="btn"][contains(.,"Удалить")]'
    RENAME_BTN = '//button[@data-bem="btn"][contains(.,"Переименовать")]'
    COPY_BTN = '//button[@data-bem="btn"][contains(.,"Скопировать")]'

    FILES_ICONS_SELECTOR = 'div.b-collection__item'
    FILES_NAMES = 'div.b-filename__text'
    FILES_LISTS_ROW = '//div[@class="DataListRow__root--bZaRr"]'

    POPUP_CLOSE_BTN = '//button[@class="btn btn_main btn_neighboring "][contains(.,"Спасибо, понятно")]'

    BIN_LINK = '//span[@class="b-nav__item__text"][contains(.,"Корзина")]'
    RESTORE_BTN = '(//span[@class="b-toolbar__btn__text b-toolbar__btn__text_pad"][contains(.,"Восстановить")])[1]'
    CLEAR_BIN_BTN = '(//span[@class="b-toolbar__btn__text b-toolbar__btn__text_pad"][contains(.,"Очистить корзину")])[1]'

    current_path = '/'
    is_first_removing = True

    @property
    def ad(self):
        return StartAd(self.driver)

    def __get_file_icon_xpath(self, file_name):
        return '//div[@data-id="{}"][@data-bem="b-thumb"]'.format(self.current_path + file_name)

    @staticmethod
    def __get_action_xpath(action):
        return '//a[@data-name="{}"][@class="b-dropdown__list__item"]'.format(action)

    def __get_folder_link_xpath(self, name):
        return '(//div[@data-id="{}"][contains(@class,"b-nav__item js-href")])[2]'.format(self.current_path + name)

    def create_folder(self, name):
        create_folder_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_FOLDER)))
        create_folder_btn.click()
        name_input = self.wait(EC.element_to_be_clickable((By.XPATH, self.NAME_INPUT)))
        name_input.send_keys(name)
        create_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_BTN)))
        create_btn.click()

    def __perform_action_on_file(self, name, action):
        file_xpath = self.__get_file_icon_xpath(name)
        file_icon = self.wait(EC.element_to_be_clickable((By.XPATH, file_xpath)))
        action_chains = ActionChains(self.driver)
        action_chains.context_click(file_icon).perform()
        action_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.__get_action_xpath(action))))
        action_link.click()

    def move_file(self, name, new_folder):
        self.__perform_action_on_file(name, 'move')
        folder_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.__get_folder_link_xpath(new_folder))))
        folder_link.click()
        move_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.MOVE_BTN)))
        move_btn.click()

    def remove_file(self, name):
        self.__perform_action_on_file(name, 'remove')
        remove_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.REMOVE_BTN)))
        remove_btn.click()
        if self.is_first_removing:
            popup_close = self.wait(EC.element_to_be_clickable((By.XPATH, self.POPUP_CLOSE_BTN)))
            popup_close.click()
            self.is_first_removing = False

    def rename_file(self, name, new_name):
        self.__perform_action_on_file(name, 'rename')
        name_input = self.wait(EC.element_to_be_clickable((By.XPATH, self.NEW_NAME_INPUT)))
        name_input.send_keys(new_name)
        rename_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.RENAME_BTN)))
        rename_btn.click()

    def copy_file(self, name, new_folder):
        self.__perform_action_on_file(name, 'copy')
        folder_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.__get_folder_link_xpath(new_folder))))
        folder_link.click()
        copy_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.COPY_BTN)))
        copy_btn.click()

    def download_file(self, name):
        self.__perform_action_on_file(name, 'download')

    def __get_files_links(self):
        files = self.driver.find_elements(By.CSS_SELECTOR, self.FILES_ICONS_SELECTOR)
        return files

    def get_files_names_list(self):
        files = self.driver.find_elements(By.CSS_SELECTOR, self.FILES_NAMES)
        return [f.text for f in files]

    def move_to_folder(self, name):
        file_links = self.__get_files_links()
        folder_link = next((f for f in file_links if f.text == name), None)
        folder_link.click()
        self.current_path += '{}/'.format(name)

    def move_to_bin(self):
        bin_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.BIN_LINK)))
        bin_link.click()
        self.current_path = '/bin/'

    def __get_bin_items_list(self):
        items_rows = self.driver.find_elements(By.XPATH, self.FILES_LISTS_ROW)
        return items_rows

    def get_bin_items_names(self):
        items = self.__get_bin_items_list()
        return [item.text for item in items]

    def clear_bin(self):
        clear_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CLEAR_BIN_BTN)))
        clear_btn.click()

    def restore_file(self, name):
        file_links = self.__get_bin_items_list()
        file_row = next((f for f in file_links if f.text == name), None)
        file_row.click()
        restore_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.RESTORE_BTN)))
        restore_btn.click()

    def go_back(self):
        self.driver.back()
        self.current_path = self.current_path[self.current_path[:-1].rfind('/'):]
