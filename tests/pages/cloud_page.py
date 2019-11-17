# coding=utf-8
from selenium.common import exceptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import time
from base_page import Page
from tests.components.app_downloading import DownloadWindow
from tests.components.auth_block import AuthBlock
from tests.components.bin import Bin
from tests.components.datalist import DataList
from tests.components.new_folder_popup import NewFolderPopup
from tests.components.rename_folder_popup import RenameFolderPopup
from tests.components.delete_popup import DeletePopup
from tests.components.file_menu import FileMenu
from tests.components.get_link_popup import GetLinkPopup
from tests.components.history_popup import HistoryPopup
from tests.components.new_folder_popup import NewFolderPopup
from tests.components.share_popup import SharePopup

from tests.components.auth_block import AuthBlock
from tests.components.copy_folder_popup import CopyFolderPopup

from tests.components.start_ad import StartAd
from tests.components.toolbars import ToolBars
from tests.components.uploading import Uploader

from tests.components.errors import Errors


class CloudPage(Page):
    BASE_URL = 'https://cloud.mail.ru/home/'
    BIN_URL = 'https://cloud.mail.ru/trashbin/'

    ERROR_MESSAGE = '//div[@class="notify-message"]'

    ERROR_404 = './/div[@class="http-error http-error_404"]'

    CREATE_FOLDER = '//div[@data-name="createFolder"]'

    NAME_INPUT = '//input[@value="Новая папка"]'
    NEW_NAME_INPUT = '//input[contains(@class,"layer__input")]'

    CREATE_BTN = '//button[@class="ui fluid primary button"][contains(.,"Создать")]'

    FILES_ICONS_SELECTOR = 'div.b-collection__item'
    FILES_NAMES = '//div[@class="b-filename__text"]'

    BIN_LINK = '//span[@class="b-nav__item__text"][contains(.,"Корзина")]'
    FOLDER_NAV_LINK = '(//div[@data-id="{}"][contains(@class,"b-nav__item js-href b-nav__item_active")])[1]'

    current_path = '/'
    previous_path = '/'
    is_first_removing = True

    def __init__(self, driver, path):
        Page.__init__(self, driver)
        self.PATH = path
        self.check = Errors(self.driver)
        self.current_path += path

    @property
    def ad(self):
        return StartAd(self.driver)

    @property
    def copy_popup(self):
        return CopyFolderPopup(self.driver)

    @property
    def bin(self):
        return Bin(self.driver)

    @property
    def toolbars(self):
        return ToolBars(self.driver)

    @property
    def get_link_popup(self):
        return GetLinkPopup(self.driver)

    @property
    def datalist(self):
        return DataList(self.driver)

    @property
    def new_folder_popup(self):
        return NewFolderPopup(self.driver)

    @property
    def rename_folder_popup(self):
        return RenameFolderPopup(self.driver)

    @property
    def delete_popup(self):
        return DeletePopup(self.driver)

    @property
    def share_popup(self):
        return SharePopup(self.driver)

    @property
    def history_popup(self):
        return HistoryPopup(self.driver)

    @property
    def auth_block(self):
        return AuthBlock(self.driver)

    def is_folder_exist(self, path):
        self.main_page()
        self.move(path)
        try:
            self.wait(until=EC.presence_of_element_located((By.XPATH, self.ERROR_404)), timeout=1)
        except exceptions.TimeoutException:
            return True
        return False

    @property
    def uploader(self):
        return Uploader(self.driver)

    @property
    def download_window(self):
        return DownloadWindow(self.driver)

    @property
    def file_menu(self):
        return FileMenu(self.driver, self)

    def error_notification_exists(self):
        try:
            self.wait(until=EC.presence_of_element_located((By.XPATH, self.ERROR_MESSAGE)))
        except exceptions.TimeoutException:
            return False
        return True

    def create_folder(self, name):
        create_folder_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_FOLDER)))
        create_folder_btn.click()
        name_input = self.wait(EC.element_to_be_clickable((By.XPATH, self.NAME_INPUT)))
        name_input.send_keys(name)
        create_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_BTN)))
        create_btn.click()
        xpath = self.FOLDER_NAV_LINK.format(self.current_path + name)
        self.wait(EC.presence_of_element_located((By.XPATH, xpath)))

    def move_to_folder(self, name):
        files_number = len(self.driver.find_elements(By.XPATH, self.FILES_NAMES))
        result = []
        for i in range(1, files_number + 1):
            file_name = self.wait(EC.presence_of_element_located(
                (By.XPATH, '({})[{}]'.format(self.FILES_NAMES, i)))).text
            if file_name == name:
                f = self.wait(EC.element_to_be_clickable(
                    (By.XPATH, '({})[{}]'.format(self.FILES_NAMES, i))))
                f.click()
                xpath = self.FOLDER_NAV_LINK.format(self.current_path + name)
                self.wait(EC.presence_of_element_located((By.XPATH, xpath)))
                self.previous_path = self.current_path
                self.current_path += '{}/'.format(name)
                break
            result.append(file_name)

    def move_to_bin(self):
        self.driver.get(self.BIN_URL)
        self.download_window.close_popup()
        self.previous_path = self.current_path
        self.current_path = '/bin/'

    def go_back(self):
        self.driver.back()
        self.current_path = self.previous_path
