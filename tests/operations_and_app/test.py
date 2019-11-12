# -*- coding: utf-8 -*-

import os

import unittest

from selenium.webdriver import DesiredCapabilities, Remote

from tests.pages.account import Account
from tests.pages.cloud_main import CloudMain
from tests.components.start_ad import StartAd


class OperationsTest(unittest.TestCase):

    def setUp(self):
        browser = os.environ.get('BROWSER', 'FIREFOX')
        self.email = os.environ['EMAIL']
        self.password = os.environ['PASSWORD']
        self.driver = Remote(
            command_executor='http://127.0.0.1:4444/wd/hub',
            desired_capabilities=getattr(DesiredCapabilities, browser).copy()
        )
        account = Account(self.driver)
        account.login(self.email, self.password, redirect='https://cloud.mail.ru')
        ad = StartAd(self.driver)
        ad.close()
        self.main_cloud = CloudMain(self.driver)
        self.main_cloud.copy_file('testfile', 'test')
        self.main_cloud.move_to_folder('test')

    def tearDown(self):
        files = self.main_cloud.get_files_names_list()
        for f in files:
            if f != 'intest':
                self.main_cloud.remove_file(f)

        if self.main_cloud.current_path == '/test/':
            self.main_cloud.move_to_folder('intest')
        else:
            self.main_cloud.go_back()

        files = self.main_cloud.get_files_names_list()
        for f in files:
            if f != 'intest':
                self.main_cloud.remove_file(f)

        self.driver.quit()

    def test_file_coping(self):
        file_name = 'testfile'
        folder_name = 'intest'

        self.main_cloud.copy_file(file_name, folder_name)
        self.main_cloud.move_to_folder(folder_name)

        files = self.main_cloud.get_files_names_list()
        assert file_name in files

    # def test_adding_index_to_duplicate(self):
    #     file_name = 'testfile'
    #     folder_name = 'intest'
    #
    #     self.main_cloud.copy_file(file_name, folder_name)
    #     self.main_cloud.copy_file(file_name, folder_name)
    #     self.main_cloud.move_to_folder(folder_name)
    #
    #     assert file_name + ' (1)' in self.main_cloud.get_files_names_list()
    #
    # def test_file_removing(self):
    #     file_name = 'testfile'
    #
    #     self.main_cloud.remove_file(file_name)
    #
    #     assert file_name not in self.main_cloud.get_files_names_list()
    #
    # def test_moving_removed_file_to_bin(self):
    #     file_name = 'testfile'
    #
    #     self.main_cloud.remove_file(file_name)
    #     self.main_cloud.move_to_bin()
    #
    #     assert file_name in self.main_cloud.get_bin_items_names()
    #
    # def test_file_moving(self):
    #     file_name = 'testfile'
    #     folder_name = 'intest'
    #
    #     self.main_cloud.move_file(file_name, folder_name)
    #     self.main_cloud.move_to_folder(folder_name)
    #
    #     assert file_name in self.main_cloud.get_files_names_list()
    #
    # def test_file_renaming(self):
    #     file_name = 'testfile'
    #     new_name = 'new_name'
    #
    #     self.main_cloud.rename_file(file_name, new_name)
    #
    #     assert new_name in self.main_cloud.get_files_names_list()

"""
Операции, допустимые над файлами

    Сохранение файла при нажатии кнопки "Скачать"
    Открытие новой вкладки с письмом и прикрепленным к нему файлом при нажатии кнопки "Отправить по почте"

Операции с корзиной

    Перемещение файла/папки в выбранную папку при нажатии кнопки Восстановить
    Добавление индекса к имени файла/папки при восстановлении в папку, где находится файл/папка с таким же именем
    Удаление всех файлов и папок из корзины при нажатии кнопки "Очистить корзину"

Операции с историей файлов

    При нажатии на кнопку “Посмотреть историю” отображается история изменений файла
    При нажатии на кнопку перезаписи/создания копии старой версии при отсутствии платной подписки отображается предупреждение

Установка приложения

    При нажатии на кнопку “Облако для ПК” появляется окно с ссылкой для скачивания клиента для соответствующей ОС
    При нажатии на кнопку “IOS” открывается страница App Store приложения “Облако Mail.ru: Галерея фото”
    При нажатии на кнопку “Android” открывается страница Google Play приложения “Облако Mail.ru: Освободи место для новых фотографий”
"""