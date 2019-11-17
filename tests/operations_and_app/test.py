# -*- coding: utf-8 -*-

import os
import platform
import time

import unittest

from selenium.webdriver import DesiredCapabilities, Remote
from selenium import webdriver

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
        self.download_folder = os.environ['DOWNLOAD_FOLDER']

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
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': self.download_folder}}
        self.driver.execute("send_command", params)

        account = Account(self.driver)
        account.login(self.email, self.password, redirect='https://cloud.mail.ru')
        ad = StartAd(self.driver)
        ad.close()
        self.cloud_page = CloudPage(self.driver, '')
        self.cloud_page.uploader.upload_file(os.path.dirname(os.path.abspath(__file__)), self.FILE_NAME)
        self.cloud_page.datalist.does_file_exist('/' + self.FILE_NAME)
        self.cloud_page.create_folder('test')
        self.cloud_page.go_back()
        time.sleep(2)
        self.cloud_page.file_menu.copy_file('testfile', 'test')
        self.cloud_page.move_to_folder('test')
        self.cloud_page.create_folder('intest')
        self.cloud_page.go_back()
        time.sleep(2)
        self.cloud_page.current_path = '/test/'
        self.cloud_page.previous_path = '/'
        self.first_deletion = True
        self.is_downloaded = False

    def tearDown(self):
        if self.cloud_page.current_path == '/bin/':
            if self.cloud_page.bin.is_empty():
                self.cloud_page.bin.clear()
            self.cloud_page.go_back()

        self.driver.get(self.cloud_page.BASE_URL)
        self.cloud_page.current_path = '/'
        self.cloud_page.file_menu.remove_file('test')
        if self.first_deletion:
            self.cloud_page.delete_popup.submit()
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)

        self.driver.quit()

    def htest_file_coping(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        files = self.cloud_page.datalist.get_files_names_list()
        self.assertIn(self.FILE_NAME, files)

    def htest_adding_index_to_duplicate(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.file_menu.copy_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        files = self.cloud_page.datalist.get_files_names_list()
        self.assertIn(self.FILE_NAME + ' (1)', files)

    def htest_file_removing(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()

        self.assertNotIn(self.FILE_NAME, self.cloud_page.datalist.get_files_names_list())

    def htest_moving_removed_file_to_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()

        files = self.cloud_page.bin.get_items_names()
        self.assertIn(self.FILE_NAME, files)

    def test_file_moving(self):
        folder_name = 'intest'

        self.cloud_page.file_menu.move_file(self.FILE_NAME, folder_name)
        self.cloud_page.move_to_folder(folder_name)

        self.assertIn(self.FILE_NAME, self.cloud_page.datalist.get_files_names_list())

    def htest_file_renaming(self):
        new_name = 'new_name'

        self.cloud_page.file_menu.rename_file(self.FILE_NAME, new_name)

        self.assertIn(new_name, self.cloud_page.datalist.get_files_names_list())

    def htest_clear_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()
        self.cloud_page.bin.clear()

        self.assertNotIn(self.FILE_NAME, self.cloud_page.bin.get_items_names())

    def htest_restoring_from_bin(self):
        self.cloud_page.file_menu.remove_file(self.FILE_NAME)
        self.first_deletion = False
        self.cloud_page.delete_popup.submit()
        self.cloud_page.move_to_bin()
        self.cloud_page.bin.restore_file(self.FILE_NAME, 'test')
        self.cloud_page.go_back()

        self.assertTrue(self.cloud_page.datalist.does_file_exist(self.cloud_page.current_path + self.FILE_NAME))

    def htest_restoring_with_index(self):
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
        self.assertTrue(self.cloud_page.datalist.does_file_exist(self.cloud_page.current_path + new_name))

    def htest_showing_history(self):
        self.cloud_page.file_menu.open_history(self.FILE_NAME)
        history = self.cloud_page.history_popup.get_history_list()
        self.cloud_page.history_popup.close()

        self.assertTrue(len(history) > 0)

    def ttest_replace_file_without_subscription(self):
        self.cloud_page.go_back()
        self.cloud_page.file_menu.open_history(self.FILE_NAME)
        self.cloud_page.history_popup.replace_with_last()

        assert not self.cloud_page.history_popup.is_replacing_allowed()

    def htest_downloading(self):
        self.cloud_page.file_menu.download_file(self.FILE_NAME)
        self.is_downloaded = wait_download(self.download_folder + self.FILE_NAME)

        self.assertTrue(self.is_downloaded)

    def htest_attaching_to_letter(self):
        self.cloud_page.file_menu.send(self.FILE_NAME)
        self.driver.switch_to.window(self.driver.window_handles[1])
        url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.assertIn('https://e.mail.ru/compose/?cloud_files_ids', url)
        self.assertIn(self.FILE_NAME, url)

    def htest_open_google_play(self):
        expected_url = 'https://play.google.com/store/apps/details?id=ru.mail.cloud'

        self.driver.refresh()
        self.cloud_page.download_window.download_for_android()
        self.driver.switch_to.window(self.driver.window_handles[1])
        current_url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.assertEqual(current_url, expected_url)

    def htest_open_app_store(self):
        expected_url = 'https://apps.apple.com/ru/app/oblako-mail-ru/id696551382'

        self.driver.refresh()
        self.cloud_page.download_window.download_for_ios()
        self.driver.switch_to.window(self.driver.window_handles[1])
        current_url = self.driver.current_url

        self.driver.switch_to.window(self.driver.window_handles[0])
        self.assertEqual(current_url, expected_url)

    def htest_open_app_downloading_page(self):
        current_os = 'mac' if platform.system() == 'Linux' else platform.system()

        self.driver.refresh()
        self.cloud_page.download_window.download_for_desktop()
        system = self.cloud_page.download_window.get_os_message()
        self.cloud_page.download_window.close_popup()

        self.assertIn(current_os, system)
