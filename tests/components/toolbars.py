# -*- coding: utf-8 -*-
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.by import By
from selenium.common.exceptions import ElementNotInteractableException

from component import Component
import os, time


class ToolBars(Component):
    DELETE_BUTTON = './/div[@data-name="remove"]'
    GET_LINK_BUTTON = './/div[@data-name="publish"]'
    TOOLBAR = '//div[@id="cloud_toolbars"]'
    CREATE_NEW_FOLDER_BUTTON = './/div[@data-name="createFolder"]'
    SHARE_BUTTON = './/div[@data-name="share"]'
    DOWNLOAD_BUTTON = './/div[@data-name="download"]'
    DISABLED = 'disabled'
    MORE_BUTTON = './/div[@title="Ещё"]'
    COPY_BUTTON = './/a[@data-name="copy"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        root_elem = self.wait(EC.presence_of_element_located((By.XPATH, self.TOOLBAR)))
        self.root = root_elem

    def delete(self):
        delete_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.DELETE_BUTTON)))
        delete_button.click()

    def get_link(self):
        get_link_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.GET_LINK_BUTTON)))
        if get_link_button.is_enabled():
            get_link_button.click()
        else:
            raise ElementNotInteractableException(msg='Button is disabled')

    def create_new_folder(self):
        create_new_folder_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.CREATE_NEW_FOLDER_BUTTON)))
        create_new_folder_button.click()

    def share(self):
        share_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.SHARE_BUTTON)))
        share_button.click()

    def is_share_button_active(self):
        share_button = self.driver.find_element_by_xpath(self.SHARE_BUTTON)
        return share_button.get_attribute(self.DISABLED) is None

    def more(self):
        more_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.MORE_BUTTON)))
        more_button.click()

    def copy(self):
        cb = self.wait(EC.element_to_be_clickable((By.XPATH, self.COPY_BUTTON)))
        cb.click()

    def download(self):
        download_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.DOWNLOAD_BUTTON)))
        download_button.click()
    
    def check_downloads(self, file_path):
         # waits for all the files to be completed and returns the paths
        time_to_wait = 30
        time_counter = 0
        print("file_path:", file_path)
        while not os.path.exists(file_path):
            time.sleep(1)
            time_counter += 1
            if time_counter > time_to_wait:return False

        print("done")
        return True

