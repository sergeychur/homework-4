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
from tests.pages.folder_page import FolderPage
from tests.components.errors import Errors

from tests.components.copy_folder_popup  import CopyFolderPopup
from tests.components.new_folder_popup  import NewFolderPopup

class CloudFolderTest(unittest.TestCase):
    NEW_FOLDER_NAME = 'new_folder' + str(uuid.uuid4())
    HOME_URL = 'https://cloud.mail.ru/home/'
    SHARED_PAGE_URL = 'https://cloud.mail.ru/shared/incoming/'
    INVALID_EMAIL = '``````\"@mail.ru'

    # create new folder with selected name and selected location
    def _new_folder(self, name, path=""):
        self.cur_cloud_page.toolbars.create_new_folder()
        new_folder_popup = NewFolderPopup(self.driver)
        print("self.HOME_URL:", self.HOME_URL)
        print("path:", path)
        new_folder_popup.create_new(name, self.HOME_URL+path)
    
    # name - name of folder
    # path - path to folder. if path is "", then folder is located in root
    # Example: we want delete folder 'c', it's located as above
    # |a| --> |b| --> |c|
    # name is "c", path is "a/b/"
    def _delete_folder(self, name, path=""):
        self.cur_cloud_page.move(path)
        self.cur_cloud_page.datalist.choose_folder_by_name('/' + self.NEW_FOLDER_NAME)
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()

    # go inside folder with selected name
    def _inside(self, name):
          self.cur_cloud_page.datalist.choose_folder_by_name('/' + name)

    # copy folder 'a' to folder 'b'
    def _copy(self, a, b):
        self.cur_cloud_page.main_page()
        self._inside(a)
        self.cur_cloud_page.toolbars.more()
        self.cur_cloud_page.toolbars.copy()
        copy_popup = CopyFolderPopup(self.driver)
        copy_popup.copy_to_folder(b)

    def _create_file_for_test(self, depth):
        for i in range(depth):
            self.cur_cloud_page.toolbars.create_new_folder()
            self.cur_cloud_page.new_folder_popup.create_new(self.NEW_FOLDER_NAME, self.HOME_URL +
                                                    (self.NEW_FOLDER_NAME + '/') * i)

    def _delete_folder(self, name):
        self.cur_cloud_page = CloudPage(self.driver, '')
        self.cur_cloud_page.open()
        self.cur_cloud_page.datalist.choose_folder_by_name('/' + name)
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()
######################
    def _prepare_for_download(self, depth):    
        self._create_file_for_test(1)
    
    # original location of folders
    #   |a| --> |c| 
    #   |b| --> |d| 
    
    # folders location after copying 
    #   |a| --> |c|
    #           |b| --> |d|
    #   |b| --> |d| 

    # a,b,c,d parameters - names of folders
    def _setup_copy_no_name(self, a="a", b="b", c="c", d="d"):  
        self.cur_cloud_page.main_page()  
        self._new_folder(a)
        self._new_folder(b, a+"/")
        self.cur_cloud_page.main_page()
        self._new_folder(c)
        self._new_folder(d, c+"/")

    # a,b,c,d parameters - names of folders
    def _clear_copy_no_name(self, a="a", b="b", c="c", d="d"):    
        self._delete_folder(a)
        self._delete_folder(c)


######################

    def setUp(self):
        before_test_map = {
            'test_delete': partial(self._create_file_for_test, 1),
            'test_copy_no_such_name': self._setup_copy_no_name,
        }

        browser = os.environ.get('BROWSER', 'CHROME')
        self.home = os.environ['HOME']
        self.downloads = os.environ.get('DOWNLOAD_FOLDER','-')
        if self.downloads == '-':
            self.downloads = self.home+("/Загрузки")
            
        print(self.downloads)
        print("self.downloads:", self.downloads)
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']
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
            'test_download': self._delete_folder,
            'test_copy_no_such_name': self._clear_copy_no_name,
        }
        after_test = after_test_map.get(self._testMethodName, None)
        if after_test is not None:
            after_test()
        self.driver.quit()

    '''
    def test_delete(self):
        # checks if public link to file is valid after it's creation
        
        self._delete_folder()
        self.folder_page = FolderPage(self.driver, self.HOME_URL + self.NEW_FOLDER_NAME)
        self.folder_page.open()
        self.assertTrue(self.folder_page.errors.isError404())

    def test_download(self):
        self.cur_cloud_page.datalist.choose_first_file()
        self.cur_cloud_page.toolbars.more()
        self.cur_cloud_page.toolbars.copy()
        copy_popup = CopyFolderPopup(self.driver)
        copy_popup.create_folder("create_folder", self.HOME_URL)
        copy_popup.copy()
        self.folder_page = FolderPage(self.driver, "create_folder"+"/")
        self.folder_page.open()
        self.cur_cloud_page.toolbars.download()
        print("self.downloads :",self.downloads)
        self.cur_cloud_page.toolbars.check_downloads(self.downloads + "create_folder.zip")
        self.assertTrue(self.folder_page.errors.isError404())
'''
    def test_copy_no_such_name(self, a="a", b="b", c="c", d="d"):
        self.cur_cloud_page.move(a+"/"+"c")
        errors = Errors(self.driver)
        self.assertTrue(errors.isError404())
        self._copy(c,a)
