# -*- coding: utf-8 -*-

import os

import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages.account import Account
from tests.components.start_ad import StartAd


class CloudFileAccessTest(unittest.TestCase):

    def setUp(self):
        browser = os.environ.get('BROWSER', 'CHROME')
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )

    def tearDown(self):
        self.driver.quit()

    def test_example(self):
        account = Account(self.driver)
        account.login(self.email, self.password, redirect='https://cloud.mail.ru')
        ad = StartAd(self.driver)
        ad.close()

