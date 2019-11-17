# coding=utf-8
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class DownloadWindow(Component):
    COMPONENT = '//div[@class="download"]'
    ANDROID_BTN = '//a[@data-name="android"]'
    IOS_BTN = '//a[@data-name="ios"]'
    DESKTOP_BTN = '//a[@class="download__apps__desktop__link download__apps__desktop__link_disko"]'
    DOWNLOAD_BTN = '//a[@target][@data-name="download"]'
    CLOSE_BTN = '//div[@class="b-panel__close"][@data-name="close"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.COMPONENT)))

    def download_for_android(self):
        btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.ANDROID_BTN)))
        self.driver.execute_script("window.scrollTo(0, {});".format(btn.location_once_scrolled_into_view['y']))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        self.driver.execute_script("window.scrollTo(0, 0);")

    def download_for_ios(self):
        btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.IOS_BTN)))
        self.driver.execute_script("window.scrollTo(0, {});".format(btn.location_once_scrolled_into_view['y']))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        self.driver.execute_script("window.scrollTo(0, 0);")

    def download_for_desktop(self):
        btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.DESKTOP_BTN)))
        self.driver.execute_script("window.scrollTo(0, {});".format(btn.location_once_scrolled_into_view['y']))
        ActionChains(self.driver).move_to_element(btn).click().perform()
        self.driver.execute_script("window.scrollTo(0, 0);")

    def get_os_message(self):
        return self.wait(EC.element_to_be_clickable((By.XPATH, self.DOWNLOAD_BTN))).text

    def close_popup(self):
        close_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.CLOSE_BTN)))
        close_btn.click()

