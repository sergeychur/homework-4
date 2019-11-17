# -*- coding: utf-8 -*-

import os
import platform
import time

import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from tests.pages.account import Account
from tests.pages.cloud_page import CloudPage
from tests.components.start_ad import StartAd


def wait_download(path, timeout=30, step=0.1):
    while not os.path.exists(path) and timeout > 0:
        time.sleep(step)
        timeout -= step
    return timeout > 0


class OperationsTest(unittest.TestCase):
    FILE_NAME = 'testfile'

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']

        prefs = {'download.prompt_for_download': False,
                 'download.directory_upgrade': True,
                 'safebrowsing.enabled': False,
                 'safebrowsing.disable_download_protection': True}

        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', prefs)
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy(),
            options=options
        )
        self.driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        self.driver.desired_capabilities['browserName'] = 'b_name'
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': r'/tmp/'}}
        self.driver.execute("send_command", params)

        account = Account(self.driver)
        account.login(self.email, self.password, redirect='https://cloud.mail.ru')
        ad = StartAd(self.driver)
        ad.close()
        self.cloud_page = CloudPage(self.driver, '')
        self.cloud_page.file_menu.copy_file('testfile', 'test')
        self.cloud_page.move_to_folder('test')
        self.first_deletion = True
        self.is_downloaded = False

    def tearDown(self):
        if self.cloud_page.current_path == '/bin/':
            if self.cloud_page.bin.is_empty():
                self.cloud_page.bin.clear()
            self.cloud_page.go_back()

        if self.cloud_page.current_path == '/':
            self.cloud_page.move_to_folder('test')

        files = self.cloud_page.datalist.get_files_names_list()
        for f in files:
            if f != 'intest':
                self.cloud_page.file_menu.remove_file(f)
                if self.first_deletion:
                    self.first_deletion = False
                    self.cloud_page.delete_popup.submit()
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

        if self.cloud_page.current_path == '/test/':
            self.cloud_page.move_to_folder('intest')
        else:
            self.cloud_page.go_back()

        files = self.cloud_page.datalist.get_files_names_list()
        for f in files:
            if f != 'intest':
                self.cloud_page.file_menu.remove_file(f)
                if self.first_deletion:
                    self.first_deletion = False
                    self.cloud_page.delete_popup.submit()
                    self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

        if self.is_downloaded:
            os.remove('/tmp/' + self.FILE_NAME)

        self.driver.quit()

    def test_file_coping(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        files = self.cloud_page.datalist.get_files_names_list()
        assert self.FILE_NAME in files

    def test_adding_index_to_duplicate(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        files = self.cloud_page.datalist.get_files_names_list()
        assert self.FILE_NAME + ' (1)' in files

    def test_file_removing(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()

        assert self.FILE_NAME not in self.cloud_page.datalist.get_files_names_list()

    def test_moving_removed_file_to_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()

        files = self.cloud_page.bin.get_items_names()
        assert self.FILE_NAME in files

    def test_file_moving(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.move_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        assert self.FILE_NAME in self.cloud_page.datalist.get_files_names_list()

    def test_file_renaming(self):
        new_name = 'new_name'

        self.cloud_page.file_menu.rename_file(self.FILE_NAME, new_name)

        assert new_name in self.cloud_page.datalist.get_files_names_list()

    def test_clear_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()
        self.cloud_page.bin.clear()

        assert self.FILE_NAME not in self.cloud_page.bin.get_items_names()

    def test_restoring_from_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()
        self.cloud_page.bin.restore_file(self.FILE_NAME, 'test')
        self.cloud_page.go_back()

        assert self.cloud_page.datalist.does_file_exist(self.cloud_page.current_path + self.FILE_NAME)

    def test_restoring_with_index(self):
        current_folder = 'test'

        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.go_back()
        self.cloud_page.file_menu.copy_file(self.FILE_NAME, current_folder)
        self.cloud_page.move_to_folder(current_folder)
        self.cloud_page.move_to_bin()
        self.cloud_page.bin.restore_file(self.FILE_NAME, current_folder)
        self.cloud_page.go_back()

        new_name = self.FILE_NAME + ' (1)'
        assert self.cloud_page.datalist.does_file_exist(self.cloud_page.current_path + new_name)

    def test_showing_history(self):
        self.cloud_page.file_menu.open_history(self.FILE_NAME)
        history = self.cloud_page.history_popup.get_history_list()
        self.cloud_page.history_popup.close()

        assert len(history) > 0

    def ttest_replace_file_without_subscription(self):
        self.cloud_page.go_back()
        self.cloud_page.file_menu.open_history(self.FILE_NAME)
        self.cloud_page.history_popup.replace_with_last()

        assert not self.cloud_page.history_popup.is_replacing_allowed()

    def test_downloading(self):
        download_path = '/tmp/'

        self.cloud_page.file_menu.download_file(self.FILE_NAME)
        self.is_downloaded = wait_download(download_path + self.FILE_NAME)

        assert self.is_downloaded

    def test_attaching_to_letter(self):
        self.cloud_page.file_menu.send(self.FILE_NAME)
        self.driver.switch_to.window(self.driver.window_handles[1])
        url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        assert 'https://e.mail.ru/compose/?cloud_files_ids' in url
        assert self.FILE_NAME in url

    def test_open_google_play(self):
        expected_url = 'https://play.google.com/store/apps/details?id=ru.mail.cloud'

        self.driver.refresh()
        self.cloud_page.download_window.download_for_android()
        self.driver.switch_to.window(self.driver.window_handles[1])
        current_url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        assert current_url == expected_url

    def test_open_app_store(self):
        expected_url = 'https://apps.apple.com/ru/app/oblako-mail-ru/id696551382'

        self.driver.refresh()
        self.cloud_page.download_window.download_for_ios()
        self.driver.switch_to.window(self.driver.window_handles[1])
        current_url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        assert current_url == expected_url

    def test_open_app_downloading_page(self):
        current_os = 'mac' if platform.system() == 'Linux' else platform.system()

        self.driver.refresh()
        self.cloud_page.download_window.download_for_desktop()
        system = self.cloud_page.download_window.get_os_message()
        self.cloud_page.download_window.close_popup()

        assert current_os in system
