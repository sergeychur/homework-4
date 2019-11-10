# -*- coding: utf-8 -*-

import os
import urllib
import uuid
import requests
import json
from functools import partial

import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages.account import Account
from tests.pages.cloud_page import CloudPage
from tests.pages.shared_page import SharedPage


def check_link(link):
    filepath = link.split('https://cloud.mail.ru/public/')[1]
    query_string = urllib.urlencode({'weblink': filepath})
    url = 'https://cloud.mail.ru/api/v2/file?{}'.format(query_string)
    resp = requests.get(url)
    decoded = json.JSONDecoder().decode(resp.content)
    return decoded


class CloudFileAccessTest(unittest.TestCase):
    NEW_FOLDER_NAME = 'new_folder' + str(uuid.uuid4())
    HOME_URL = 'https://cloud.mail.ru/home/'
    SHARED_PAGE_URL = 'https://cloud.mail.ru/shared/incoming/'
    INVALID_EMAIL = '``````\"@mail.ru'

    def _create_file_for_test(self, depth):
        for i in range(depth):
            self.cur_cloud_page.toolbars.create_new_folder()
            self.cur_cloud_page.new_folder_popup.create_new(self.NEW_FOLDER_NAME, self.HOME_URL +
                                                            (self.NEW_FOLDER_NAME + '/') * i)

    def _delete_folder(self):
        self.cur_cloud_page = CloudPage(self.driver, '')
        self.cur_cloud_page.open()
        self.cur_cloud_page.datalist.choose_folder_by_name('/' + self.NEW_FOLDER_NAME)
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()

    def _grant_access_and_change_user(self):
        self.depth = 2
        self._create_file_for_test(depth=self.depth)
        self.driver.back()
        self.cur_cloud_page.toolbars.share()
        self.cur_cloud_page.share_popup.fill_name(self.other_user_email)
        self.cur_cloud_page.share_popup.choose_access_type('view_only')
        self.cur_cloud_page.share_popup.accept()
        self.cur_cloud_page.share_popup.close()
        self.cur_cloud_page.auth_block.logout()
        self.account.login(self.other_user_email, self.other_user_pass)

        self.shared_page = SharedPage(self.driver)
        self.shared_page.open()
        self.shared_page.close_annoying_adverts()
        self.shared_page.invitation_list.accept_by_name(self.NEW_FOLDER_NAME)
        self.shared_page.accept_popup.accept()
        self.shared_page.invitation_list.wait_till_accepted(self.NEW_FOLDER_NAME)
        self.cur_cloud_page = CloudPage(self.driver, self.NEW_FOLDER_NAME)
        self.cur_cloud_page.open()
        self.cur_cloud_page.ad.close()

    def _clear_after_change_user(self):
        self.cur_cloud_page.delete_popup.close()
        self.cur_cloud_page.auth_block.logout()
        self.account.login(self.email, self.password)
        self._delete_folder()

    def setUp(self):
        before_test_map = {
            'test_deleted_file_link': partial(self._create_file_for_test, 1),
            'test_access_to_root_folder': partial(self._create_file_for_test, 1),
            'test_access_to_deep_folder': partial(self._create_file_for_test, 3),
            'test_access_to_invalid_user': partial(self._create_file_for_test, 1),
            'test_invalid_delete': self._grant_access_and_change_user,
        }

        browser = os.environ.get('BROWSER', 'CHROME')
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']
        self.other_user_email = os.environ['OTHER_USER_EMAIL']
        self.other_user_pass = os.environ['OTHER_USER_PASS']
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        self.account = Account(self.driver)
        self.account.login(self.email, self.password, redirect=self.HOME_URL)
        self.cur_cloud_page = CloudPage(self.driver, '')
        self.cur_cloud_page.ad.close()
        before_test = before_test_map.get(self._testMethodName, None)
        if before_test is not None:
            before_test()

    def tearDown(self):
        after_test_map = {
            'test_access_to_root_folder': self._delete_folder,
            'test_access_to_deep_folder': self._delete_folder,
            'test_access_to_invalid_user': self._delete_folder,
            'test_invalid_delete': self._clear_after_change_user,
        }
        after_test = after_test_map.get(self._testMethodName, None)
        if after_test is not None:
            after_test()
        self.driver.quit()

    def test_public_link(self):
        # checks if public link to file is valid after it's creation
        self.cur_cloud_page.datalist.choose_first_file()
        self.cur_cloud_page.toolbars.get_link()
        link = self.cur_cloud_page.get_link_popup.get_link_value()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.ok)

    def test_public_link_revoke(self):
        # checks if the public link to file is still valid(doesn't return 404) after revoking access
        # (it shouldn't)
        self.cur_cloud_page.datalist.choose_first_file()
        self.cur_cloud_page.toolbars.get_link()
        link = self.cur_cloud_page.get_link_popup.get_link_value()
        self.cur_cloud_page.get_link_popup.close_access()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.not_found)

    def test_deleted_file_link(self):
        # checks if the public link is still valid after file removing
        # (it shouldn't)
        self.cur_cloud_page.toolbars.get_link()
        link = self.cur_cloud_page.get_link_popup.get_link_value()
        self.cur_cloud_page.get_link_popup.close_popup()
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.not_found)

    def test_access_to_root_folder(self):
        # tests if it is possible to grant access to folder which is in
        # root folder to concrete user
        share_button_active = self.cur_cloud_page.toolbars.is_share_button_active()
        self.assertTrue(share_button_active)

    def test_access_to_deep_folder(self):
        # tests if it is possible to grant access to folder which is in
        # folder deeper then root folder to concrete user
        share_button_active = self.cur_cloud_page.toolbars.is_share_button_active()
        self.assertTrue(share_button_active)

    def test_access_to_invalid_user(self):
        # tests if it is possible to grant access on to user whose name is definitely invalid
        self.cur_cloud_page.toolbars.share()
        self.cur_cloud_page.share_popup.fill_name(self.INVALID_EMAIL)
        self.cur_cloud_page.share_popup.accept()
        error_exists = self.cur_cloud_page.share_popup.is_error_exist()
        self.assertTrue(error_exists)

    def test_invalid_delete(self):
        # user is granted to view smth, he tries to delete it, should not succeed
        self.cur_cloud_page.datalist.choose_folder_by_name(('/' + self.NEW_FOLDER_NAME) * self.depth)
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()
        error_exists = self.cur_cloud_page.error_notification_exists()
        self.assertTrue(error_exists)
