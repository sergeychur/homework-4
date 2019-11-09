# -*- coding: utf-8 -*-

import os
import urllib
import requests
import json

import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages.account import Account
from tests.pages.cloud_main import CloudMain


def check_link(link):
    filepath = link.split('https://cloud.mail.ru/public/')[1]
    query_string = urllib.urlencode({'weblink': filepath})
    url = 'https://cloud.mail.ru/api/v2/file?{}'.format(query_string)
    resp = requests.get(url)
    decoded = json.JSONDecoder().decode(resp.content)
    return decoded


class CloudFileAccessTest(unittest.TestCase):
    NEW_FOLDER_NAME = 'new_folder'
    HOME_URL = 'https://cloud.mail.ru/home/'

    def create_file_for_test(self):
        self.cloud_main.toolbars.create_new_folder()
        self.cloud_main.new_folder_popup.create_new(self.NEW_FOLDER_NAME, self.HOME_URL)

    def setUp(self):
        self.before_test_map = {
            'test_deleted_file_link': self.create_file_for_test
        }

        browser = os.environ.get('BROWSER', 'CHROME')
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        self.account = Account(self.driver)
        self.account.login(self.email, self.password, redirect=self.HOME_URL)
        self.cloud_main = CloudMain(self.driver)
        self.cloud_main.ad.close()
        before_test = self.before_test_map.get(self._testMethodName, None)
        if before_test is not None:
            before_test()

    def tearDown(self):
        self.driver.quit()

    def test_public_link(self):
        # checks if public link to file is valid after it's creation
        self.cloud_main.datalist.choose_first_file()
        self.cloud_main.toolbars.get_link()
        link = self.cloud_main.get_link_popup.get_link_value()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.ok)

    def test_public_link_revoke(self):
        # checks if the public link to file is still valid(doesn't return 404) after revoking access
        # (it shouldn't)
        self.cloud_main.datalist.choose_first_file()
        self.cloud_main.toolbars.get_link()
        link = self.cloud_main.get_link_popup.get_link_value()
        self.cloud_main.get_link_popup.close_access()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.not_found)

    def test_deleted_file_link(self):
        # checks if the public link is still valid after file removing
        # (it shouldn't)
        self.cloud_main.toolbars.get_link()
        link = self.cloud_main.get_link_popup.get_link_value()
        self.cloud_main.get_link_popup.close_popup()
        self.cloud_main.toolbars.delete()
        self.cloud_main.delete_popup.accept()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.not_found)
