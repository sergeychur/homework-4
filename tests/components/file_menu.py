# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class FileMenu(Component):
    MOVE_BTN = '//button[@data-bem="btn"][contains(.,"Переместить")]'
    REMOVE_BTN = '//button[@data-bem="btn"][contains(.,"Удалить")]'
    RENAME_BTN = '//button[@data-bem="btn"][contains(.,"Переименовать")]'
    SEND_BTN = '//a[@data-bem="b-dropdown__list__params"][contains(.,"Отправить по почте")]'
    COPY_BTN = '//button[@data-bem="btn"][contains(.,"Скопировать")]'
    NEW_NAME_INPUT = '//input[contains(@class,"layer__input")]'
    HIDDEN_MENU = '//div[@class="b-dropdown__list b-dropdown__list_contextmenu"][contains(@style, "z-index: 0")]'

    def __init__(self, driver, page):
        Component.__init__(self, driver=driver)
        self.page = page

    def __get_file_icon_xpath(self, file_name):
        return '//div[@data-id="{}"][@data-bem="b-thumb"]'.format(self.page.current_path + file_name)

    @staticmethod
    def __get_action_xpath(action):
        return '//a[@data-name="{}"][@class="b-dropdown__list__item"]'.format(action)

    def __get_folder_link_xpath(self, name):
        return '(//div[@data-id="{}"][contains(@class,"b-nav__item js-href")])[2]'.format(self.page.current_path + name)

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
        self.__wait_menu_hide()

    def remove_file(self, name):
        self.__perform_action_on_file(name, 'remove')
        remove_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.REMOVE_BTN)))
        remove_btn.click()
        self.__wait_menu_hide()

    def rename_file(self, name, new_name):
        self.__perform_action_on_file(name, 'rename')
        name_input = self.wait(EC.element_to_be_clickable((By.XPATH, self.NEW_NAME_INPUT)))
        name_input.send_keys(new_name)
        rename_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.RENAME_BTN)))
        rename_btn.click()
        self.__wait_menu_hide()
        file_xpath = self.__get_file_icon_xpath(new_name)
        self.wait(EC.presence_of_element_located((By.XPATH, file_xpath)))

    def copy_file(self, name, new_folder):
        self.__perform_action_on_file(name, 'copy')
        folder_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.__get_folder_link_xpath(new_folder))))
        folder_link.click()
        copy_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.COPY_BTN)))
        copy_btn.click()
        self.__wait_menu_hide()

    def open_history(self, name):
        self.__perform_action_on_file(name, 'history')

    def download_file(self, name):
        self.__perform_action_on_file(name, 'download')

    def __wait_menu_hide(self):
        self.wait(EC.presence_of_element_located((By.XPATH, self.HIDDEN_MENU)))

    def send(self, name):
        file_xpath = self.__get_file_icon_xpath(name)
        file_icon = self.wait(EC.element_to_be_clickable((By.XPATH, file_xpath)))
        action_chains = ActionChains(self.driver)
        action_chains.context_click(file_icon).perform()
        action_link = self.wait(EC.element_to_be_clickable((By.XPATH, self.SEND_BTN)))
        action_link.click()
