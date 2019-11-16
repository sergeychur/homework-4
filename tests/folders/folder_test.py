# -*- coding: utf-8 -*-

import os
import urllib
import uuid
import requests
import json
from functools import partial

import unittest
import time

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
        new_folder_popup.create_new(name, self.HOME_URL+path)
    
    def _new_folder_no_wait(self, name, path=""):
        self.cur_cloud_page.toolbars.create_new_folder()
        new_folder_popup = NewFolderPopup(self.driver)
        new_folder_popup.create_new_no_wait(name, self.HOME_URL+path)

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
    def _action(self, a, b, copy=True):
        self.cur_cloud_page.main_page()
        self.cur_cloud_page.move(a)
        self.cur_cloud_page.toolbars.more()
        if copy:
            self.cur_cloud_page.toolbars.copy()
        else:
            self.cur_cloud_page.toolbars.move()
        copy_popup = CopyFolderPopup(self.driver, copy)
        copy_popup.copy_to_folder(b, copy)
        
    # copy folder 'a' to folder 'b'
    def _copy(self, a, b):
        self._action(a,b,True)

    # move folder 'a' inside folder 'b'
    def _replace(self, a, b):
        self._action(a,b,False)

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
    def _clear_copy_no_name(self, a="a", c="c"):    
        self._delete_folder(a)
        self._delete_folder(c)

    # original location of folders
    #   |a| --> |b| 
    #   |b| --> |c| 
    
    # folders location after copying 
    #   |a| --> |b    |
    #           |b (1)| --> |c|
    #   |b| --> |c|

    # a,b1,b2,c parameters - names of folders
    def _setup_copy_new_name(self, a="a", b1="b", b2="b", c="c"):  
        self.cur_cloud_page.main_page()  
        self._new_folder(a)
        self._new_folder(b1, a+"/")
        self.cur_cloud_page.main_page()
        self._new_folder(b2)
        self._new_folder(c, b2+"/")

    # a,b,c,d parameters - names of folders
    def _clear_copy_new_name(self, a="a", c="c"):    
        self._clear_copy_no_name(a, c)

    # original location of folders
    #   |a| --> |c| 
    #   |b| --> |d| 
    
    # folders location after copying 
    #   |a| --> |c|
    #           |b| --> |d|

    # a,b,c,d parameters - names of folders
    def _setup_move_no_name(self, a="a", b="b", c="c", d="d"):  
        self._setup_copy_no_name(a,b,c,d)

    # a,b,c,d parameters - names of folders
    def _clear_move_no_name(self, a="a"):    
        self._delete_folder(a)

    
    # original location of folders
    #   |a| --> |b| 
    #   |b| --> |c| 
    
    # folders location after copying 
    #   |a| --> |b    |
    #           |b (1)| --> |c|

    # a,b1,b2,c parameters - names of folders
    def _setup_move_new_name(self, a="a", b1="b", b2="b", c="c"):  
        self.cur_cloud_page.main_page()  
        self._new_folder(a)
        self._new_folder(b1, a+"/")
        self.cur_cloud_page.main_page()
        self._new_folder(b2)
        self._new_folder(c, b2+"/")

    # a,b,c,d parameters - names of folders
    def _clear_move_new_name(self, a="a"):    
        self._clear_move_no_name(a)


######################

    def setUp(self):
        before_test_map = {
            'test_delete': partial(self._create_file_for_test, 1),
            'test_copy_no_such_name': self._setup_copy_no_name,
            'test_copy_with_such_name': self._setup_copy_new_name,
            'test_replace_no_such_name': self._setup_move_no_name,
            'test_replace_with_such_name': self._setup_move_new_name,
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
            'test_copy_with_such_name': self._clear_copy_new_name,
            'test_replace_no_such_name': self._clear_move_no_name,
            'test_replace_with_such_name': self._clear_move_new_name,
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

    '''
    При нажатии на кнопку ‘Копировать’ и выборе папки, в которой нет 
     папки с таким же названии, в выбранной папке создается папка с 
     тем же содержимым и тем же названием.
    ''''''
    def test_copy_no_such_name(self, a="a", b="b", c="c", d="d"):
        cInA = a + "/" + c
        bInA = a + "/" + b
        dInC = c + "/" + d
        dInAC=  a +"/" + c + "/" + d
        self.assertFalse(self.cur_cloud_page.is_folder_exist(cInA))
        print("c location: home/c")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(dInC))
        print("d location: home/c/d")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(bInA))
        print("b location: home/a/b")

        self._copy(c,a)
        print("copy 'c' to 'a'")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInA))
        print("c location: home/a/c")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(dInAC))
        print("d location: home/a/c/d")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(bInA))
        print("b location: home/a/b")
    
    ''''''
    При нажатии на кнопку ‘Копировать’ и выборе папки, в которой есть
     папка с таким же названием, в выбранной папке создается папка с
     тем же содержимым и измененным названием.
    ''''''
    def test_copy_with_such_name(self, a="a", b1="b", b2="b", c="c"):
        b1InA = a + "/" + b1
        b2InA = a + "/" + "b (1)"
        cInB2 = b2 + "/" + c
        cInAB = a + "/" + "b (1)" + "/" + c
       
        self.assertTrue(self.cur_cloud_page.is_folder_exist(b1InA))
        print("first b location: home/a/b")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(b2))
        print("second b location: home/b")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInB2))
        print("c location: home/b/c")

        self._copy(b2,a)
        print("copy 'b' to 'a'")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(b1InA))
        print("first b location: home/a/b")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(b2InA))
        print("second b location: home/a/b (1)")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInAB))
        print("second b location: home/a/b (1)/c")

    ''''''
    def test_replace_no_such_name(self, a="a", b="b", c="c", d="d"):
        cInA = a + "/" + c
        bInA = a + "/" + b
        dInC = c + "/" + d
        dInAC= a +"/" + c + "/" + d

        self.assertTrue(self.cur_cloud_page.is_folder_exist(c))
        print("c location: home/c")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(dInC))
        print("d location: home/c/d")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(bInA))
        print("b location: home/a/b")

        self._replace(c,a)
        print("move 'c' to 'a'")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInA))
        self.assertFalse(self.cur_cloud_page.is_folder_exist(c))
        print("c location: home/a/c")

        self.assertFalse(self.cur_cloud_page.is_folder_exist(dInC))
        self.assertTrue(self.cur_cloud_page.is_folder_exist(dInAC))
        print("d location: home/a/c/d")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(bInA))
        print("b location: home/a/b")

    ''''''
    При нажатии на кнопку ‘Переместить’ и выборе папки, в которой есть папка с таким
     же названием, в выбранной папке создается папка с тем же содержимым и измененным
     названием, а из старой папки данная папка удаляется
    ''''''
    def test_replace_with_such_name(self, a="a", b1="b", b2="b", c="c"):
        b1InA = a + "/" + b1
        b2InA = a + "/" + "b (1)"
        cInB2 = b2 + "/" + c
        cInAB = a + "/" + "b (1)" + "/" + c
       
        self.assertTrue(self.cur_cloud_page.is_folder_exist(b1InA))
        print("first b location: home/a/b")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(b2))
        print("second b location: home/b")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInB2))
        print("c location: home/b/c")

        self._replace(b2,a)
        print("copy 'b' to 'a'")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(b1InA))
        print("first b location: home/a/b")

        self.assertFalse(self.cur_cloud_page.is_folder_exist(b2))
        self.assertTrue(self.cur_cloud_page.is_folder_exist(b2InA))
        print("second b location: home/a/b (1)")

        self.assertTrue(self.cur_cloud_page.is_folder_exist(cInAB))
        print("second b location: home/a/b (1)/c")

    '''
    
'''
    def test_create_folder_with_too_long_name(self):
        a = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
        self._new_folder_no_wait(a)
        self.cur_cloud_page.move(a)
        errors = Errors(self.driver)
        self.assertTrue(errors.isError404())
'''