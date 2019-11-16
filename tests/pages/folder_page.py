from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from base_page import Page
from tests.components.errors import Errors


class FolderPage(Page):
    BASE_URL = 'https://cloud.mail.ru/home/'
    ERROR_MESSAGE = '//div[@class="notify-message"]'

    def __init__(self, driver, path):
        Page.__init__(self, driver)
        self.BASE_URL +=  path + "/"

    @property
    def errors(self):
        return Errors(self.driver)

    def every_downloads_chrome(self, driver):
        if not driver.current_url.startswith("chrome://downloads"):
            driver.get("chrome://downloads/")
        return driver.execute_script("""
            var items = downloads.Manager.get().items_;
            if (items.every(e => e.state === "COMPLETE"))
                return items.map(e => e.fileUrl || e.file_url);
            """)
    
    def _check_downloads(self):
         # waits for all the files to be completed and returns the paths
        paths = WebDriverWait(driver, 120, 1).until(every_downloads_chrome)
        print(paths)

