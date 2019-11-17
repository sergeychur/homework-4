import platform

from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component
import pyautogui


class Uploader(Component):
    UPLOAD_CIRCLE = '//div[@class="UploadDropArea__circle--2tpLL"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.UPLOAD_CIRCLE)))

    def upload_file(self, path, name):
        upload_circle = self.wait(EC.presence_of_element_located((By.XPATH, self.UPLOAD_CIRCLE)))
        ActionChains(self.driver).move_to_element(upload_circle).click().perform()

        if 'Windows' not in platform.platform():
            pyautogui.write(path + '/' + name)
        else:
            pyautogui.write(path + '\\' + name)
        pyautogui.press('enter')
