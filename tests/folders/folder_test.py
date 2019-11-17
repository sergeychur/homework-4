# -*- coding: utf-8 -*-

import os
import urllib
import uuid
import requests
import json
from functools import partial

import unittest
import time

import random
import string
import requests

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages.account import Account
from tests.pages.cloud_page import CloudPage
from tests.pages.folder_page import FolderPage
from tests.components.errors import Errors

from tests.components.copy_folder_popup  import CopyFolderPopup
from tests.components.new_folder_popup  import NewFolderPopup
from tests.components.rename_folder_popup  import RenameFolderPopup

def check_link(link):
    filepath = link.split('https://cloud.mail.ru/public/')[1]
    query_string = urllib.urlencode({'weblink': filepath})
    url = 'https://cloud.mail.ru/api/v2/file?{}'.format(query_string)
    resp = requests.get(url)
    decoded = json.JSONDecoder().decode(resp.content)
    return decoded

class CloudFolderTest(unittest.TestCase):
    NEW_FOLDER_NAME = 'new_folder' + str(uuid.uuid4())
    HOME_URL = 'https://cloud.mail.ru/home/'
    SHARED_PAGE_URL = 'https://cloud.mail.ru/shared/incoming/'


    # create new folder with selected name and selected location
    def _rename_folder(self, new_name, path=""):
        self.cur_cloud_page.main_page()
        self.cur_cloud_page.move(path)
        self.cur_cloud_page.toolbars.more()
        self.cur_cloud_page.toolbars.rename()
        rename_folder_popup = RenameFolderPopup(self.driver)
        rename_folder_popup.rename_no_wait(new_name, self.HOME_URL+path)
        self.cur_cloud_page.main_page()
      
    # create new folder with selected name and selected location
    def _new_folder(self, name, path="", no_wait=False, back_to_root=False):
        if back_to_root:
            self.cur_cloud_page.main_page()
        self.cur_cloud_page.toolbars.create_new_folder()
        new_folder_popup = NewFolderPopup(self.driver)
        if no_wait:
            new_folder_popup.create_new_no_wait(name, self.HOME_URL+path)
        else:
            new_folder_popup.create_new(name, self.HOME_URL+path)

    def _recreate(self, name, path="", no_wait=False, back_to_root=False):
        self._delete_folder_no_wait(name, path)
        self._new_folder(name, path, no_wait, back_to_root)

    # name - name of folder
    # path - path to folder. if path is "", then folder is located in root
    # Example: we want delete folder 'c', it's located as above
    # |a| --> |b| --> |c|
    # name is "c", path is "a/b/"
    def _delete_folder(self, name, path=""):
        self.cur_cloud_page.move(path)
        self.cur_cloud_page.datalist.choose_folder_by_name('/' + name)
        self.cur_cloud_page.toolbars.delete()
        self.cur_cloud_page.delete_popup.accept()
        self.cur_cloud_page.main_page()

    def _delete_folder_no_wait(self, name, path=""):
        self.cur_cloud_page.move(path)
        if self.cur_cloud_page.datalist.choose_no_wait('/' + name):
            self.cur_cloud_page.toolbars.delete()
            self.cur_cloud_page.delete_popup.accept()
            self.cur_cloud_page.main_page()

    # go inside folder with selected name
    def _inside(self, name):
          self.cur_cloud_page.datalist.choose_folder_by_name('/' + name)

    # rename folder 'a' to 'b'
    def _rename(self, a, b):
        self.cur_cloud_page.main_page()
        self.cur_cloud_page.move(a)
        self.cur_cloud_page.toolbars.more()
        self.cur_cloud_page.toolbars.rename()

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
        self._recreate(a)
        self._new_folder(b, a+"/")
        self.cur_cloud_page.main_page()
        self._recreate(c)
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
        self._recreate(a)
        self._new_folder(b1, a+"/")
        self.cur_cloud_page.main_page()
        self._recreate(b2)
        self._new_folder(c, b2+"/")

    # a,b,c,d parameters - names of folders
    def _clear_copy_new_name(self, a="a", c="b"):    
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

    def _setup_rename(self):
        self._recreate("rename")
    
    def _clear_rename(self):
        self._clear_move_no_name("rename")
    
    def _setup_link(self):
        self._recreate("link")
    
    def _clear_link(self):
        self._delete_folder("link")

    def _setup_link2(self):
        self._recreate("link2")
    
    def _clear_link2(self):
        self._delete_folder("link2")
    '''
    def _check_symbol(self, blacklist):
        for symbol in string.ascii_letters:
            name = "test_check "+symbol+" "
            if symbol in blacklist:
                self._new_folder(name, "", True, True)
                #self.assertFalse(self.cur_cloud_page.is_folder_exist(name))
            else:
                self._new_folder(name, "", False, True)
                self._delete_folder(name)
                #self.assertTrue(self.cur_cloud_page.is_folder_exist(name))
    self._check_symbol("*/:<>.?\|")
    '''    


######################

    def setUp(self):
       
        before_test_map = {
            'test_delete': self._setup_link,
            'test_download': self._setup_link,
            'test_copy_no_such_name': self._setup_copy_no_name,
            'test_copy_with_such_name': self._setup_copy_new_name,
            'test_replace_no_such_name': self._setup_move_no_name,
            'test_replace_with_such_name': self._setup_move_new_name,
            'test_rename_folder_with_too_long_name':  self._setup_rename,
            'test_rename_folder_with_blank_name': self._setup_rename,
            'test_rename_folder_with_changed_name': self._setup_rename,
            'test_rename_folder_with_invalid_symbols': self._setup_rename,
            'test_public_link': self._setup_link,
            'test_public_link_revoke': self._setup_link2,
        }

        browser = os.environ.get('BROWSER', 'CHROME')
        self.home = os.environ['HOME']
        self.downloads = os.environ.get('DOWNLOAD_FOLDER','-')
        if self.downloads == '-':
            self.downloads = self.home+("/Загрузки")
            
        print(self.downloads)
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
            'test_download': self._clear_link,
            'test_copy_no_such_name': self._clear_copy_no_name,
            'test_copy_with_such_name': self._clear_copy_new_name,
            'test_replace_no_such_name': self._clear_move_no_name,
            'test_replace_with_such_name': self._clear_move_new_name,
            'test_rename_folder_with_blank_name': self._clear_rename,
            'test_rename_folder_with_invalid_symbols': self._clear_rename,
            'test_public_link': self._clear_link,
            'test_public_link_revoke': self._clear_link2,
        }
        after_test = after_test_map.get(self._testMethodName, None)
        if after_test is not None:
            after_test()
        self.driver.quit()

    def _buildblock(self, size):
        return ''.join(random.choice(string.ascii_letters) for _ in range(size))

    '''
    При нажатии на кнопку ‘Удалить’ папка с файлами удаляется.
    '''
    def test_delete(self):
        self.cur_cloud_page.main_page()
        self._delete_folder("link")
        self.folder_page = FolderPage(self.driver, self.HOME_URL + self.NEW_FOLDER_NAME)
        self.folder_page.open()
        self.assertTrue(self.folder_page.errors.isError404())
    
    '''
    При нажатии на кнопку ‘Скачать’ загружается архив со всеми файлами из папки
    '''
    def test_download(self):
        #self.cur_cloud_page.main_page()
        self.cur_cloud_page.move('link')
        self.cur_cloud_page.toolbars.more()
        self.cur_cloud_page.toolbars.copy()
        copy_popup = CopyFolderPopup(self.driver)
        copy_popup.create_folder("create_folder", self.HOME_URL)
        copy_popup.copy()
        self.folder_page = FolderPage(self.driver, "create_folder"+"/")
        self.folder_page.open()
        self.cur_cloud_page.toolbars.download()
        self.cur_cloud_page.toolbars.check_downloads(self.downloads + "create_folder.zip")
    
    '''
    При нажатии на кнопку ‘Копировать’ и выборе папки, в которой нет 
     папки с таким же названии, в выбранной папке создается папка с 
     тем же содержимым и тем же названием.
    '''
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
    
    '''
    При нажатии на кнопку ‘Копировать’ и выборе папки, в которой есть
     папка с таким же названием, в выбранной папке создается папка с
     тем же содержимым и измененным названием.
    '''
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
 
    '''
    При нажатии на кнопку ‘Копировать’ и выборе папки, в которой есть 
    папка с таким же названием, в выбранной папке создается папка с тем
    же содержимым и измененным названием.
    '''
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

    '''
    При нажатии на кнопку ‘Переместить’ и выборе папки, в которой есть папка с таким
     же названием, в выбранной папке создается папка с тем же содержимым и измененным
     названием, а из старой папки данная папка удаляется
    '''
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
    Все тесты связанные с созданием папок или их переименованием должны быть
    юнит тестами, но на всякий случай для этих действий были написаны ui тесты.

    ''''''
    При вводе слишком длинного названия папки, операция создания папки завершается с ошибкой
    ''' 
    def test_create_folder_with_too_long_name(self):
        not_allowed = self._buildblock(256)
        self._new_folder(name=not_allowed, no_wait=True)
        self.cur_cloud_page.move(not_allowed)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(not_allowed))
        print("A folder with a name of 256 characters can't be created")
        print("more: https://help.mail.ru/cloud_web/confines")

        allowed = self._buildblock(255)
        self.cur_cloud_page.main_page()
        self._new_folder(allowed)
        self.cur_cloud_page.move(allowed)
        self.assertTrue( self.cur_cloud_page.is_folder_exist(allowed))
        self._delete_folder(allowed)
        print("A folder with a name of 255 characters can be created")

    ''' 
    При вводе пустого имени, операция создания папки завершается с ошибкой
    ''' 
    def test_create_folder_with_blank_name(self):
        not_allowed = " "
        self._new_folder(name=not_allowed, no_wait=True)
        self.assertFalse(self.cur_cloud_page.is_folder_exist(not_allowed))

    ''' 
    При вводе названия с пробелами в начале и в конце имени папки, название 
     папки урезается до версии без пробелов в начале и конце.
    ''' 
    def test_create_folder_with_changed_name(self):
        without_blanks = self._buildblock(10)
        with_blanks = " "+without_blanks+" "
        self._new_folder(name=with_blanks, no_wait=True)
        self.assertTrue( self.cur_cloud_page.is_folder_exist(without_blanks))
        self._delete_folder(without_blanks)

    '''
    При вводе названия с запрещенными символами «" * / : < > ? \ |». операция
     создания папки завершается с ошибкой
    '''
    def test_create_folder_with_invalid_symbols(self):
        first = "some*"
        self._new_folder(first, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(first))
        
        second = "second/"
        self._new_folder(second, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(second))

        third = "third:"
        self._new_folder(third, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(third))

        forth = "forth<"
        self._new_folder(forth, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(forth))

        fifth = "fifth>"
        self._new_folder(fifth, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(fifth))

        sixth = "sixth?"
        self._new_folder(sixth, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(sixth))

        seventh = "seventh\ "
        self._new_folder(seventh, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(seventh))

        eighth = "eighth|"
        self._new_folder(eighth, "", True, True)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(eighth))
    

    '''
    этот тест не может быть успешно пройден, поскольку на облаке присутствует баг
    Запрещено создавать папки длинною более 255 байтов и этот тест проверяет,
    что запрещено и переименовывать папки в столь длинные имена
    однако при переименовании сервер не выдает ошибки а переименовывает папку,
    обрезая ее имя до допустимого размера(255). Тест падает на проверке, осталась
    ли папка с оригинальным названием
    '''
    @unittest.expectedFailure
    def test_rename_folder_with_too_long_name(self):
        main = "rename"

        allowed = self._buildblock(255)
        self._rename_folder(allowed, main)
        self.assertTrue(self.cur_cloud_page.is_folder_exist(allowed))
        print("A folder with a name of 255 characters can be created")
        
        self._rename_folder(main, allowed)

        not_allowed = self._buildblock(256)
        self._rename_folder(not_allowed, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(not_allowed))
        print("A folder with a name of 256 characters can't be created")
        print("more: https://help.mail.ru/cloud_web/confines")

        self.assertTrue( self.cur_cloud_page.is_folder_exist(main))

    ''' 
    При вводе пустого имени, операция создания папки завершается с ошибкой
    ''' 
    def test_rename_folder_with_blank_name(self):
        main = "rename"
        not_allowed = " "
        self._rename_folder(not_allowed, main)
        self.assertFalse(self.cur_cloud_page.is_folder_exist(not_allowed))

    ''' 
    При вводе названия с пробелами в начале и в конце имени папки, название 
     папки урезается до версии без пробелов в начале и конце.
    '''  
    def test_rename_folder_with_changed_name(self):
        main = "rename"
        without_blanks = self._buildblock(10)
        with_blanks = " "+without_blanks+" "
        self._rename_folder(with_blanks, main)
        self.assertTrue( self.cur_cloud_page.is_folder_exist(without_blanks))
        self._delete_folder(without_blanks)

    ''' 
    При вводе названия с запрещенными символами «" * / : < > ? \ |». операция
     создания папки завершается с ошибкой
    '''  
    def test_rename_folder_with_invalid_symbols(self):
        main = "rename"
        first = "some*"
        self._rename_folder(first, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(first))
        
        second = "second/"
        self._rename_folder(second, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(second))

        third = "third:"
        self._rename_folder(third, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(third))

        forth = "forth<"
        self._rename_folder(forth, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(forth))

        fifth = "fifth>"
        self._rename_folder(fifth, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(fifth))

        sixth = "sixth?"
        self._rename_folder(sixth, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(sixth))

        seventh = "seventh\ "
        self._rename_folder(seventh, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(seventh))

        eighth = "eighth|"
        self._rename_folder(eighth, main)
        self.assertFalse( self.cur_cloud_page.is_folder_exist(eighth))

        self.assertTrue( self.cur_cloud_page.is_folder_exist(main))
    
    '''
    При нажатии на кнопку ‘Получить ссылку’ создается ссылка с доступом к папке.
    '''
    def test_public_link(self):
        # checks if public link to file is valid after it's creation
        self.cur_cloud_page.main_page()
        self.cur_cloud_page.datalist.choose_folder_by_name("/link")
        self.cur_cloud_page.toolbars.get_link()
        link = self.cur_cloud_page.get_link_popup.get_link_value()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.ok)

    ''' 
    При нажатии на кнопку ‘Удалить ссылку’ ссылка с доступом к папке удаляется.
    ''' 
    def test_public_link_revoke(self):
        # checks if the public link to file is still valid(doesn't return 404) after revoking access
        self.cur_cloud_page.main_page()
        self.cur_cloud_page.datalist.choose_folder_by_name("/link2")
        self.cur_cloud_page.toolbars.get_link()
        link = self.cur_cloud_page.get_link_popup.get_link_value()
        self.cur_cloud_page.get_link_popup.close_access()
        decoded = check_link(link)
        self.assertEqual(decoded.get('status', requests.codes.not_found), requests.codes.not_found)
