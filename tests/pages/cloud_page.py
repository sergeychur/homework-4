from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from base_page import Page
from tests.components.start_ad import StartAd
from tests.components.toolbars import ToolBars
from tests.components.get_link_popup import GetLinkPopup
from tests.components.datalist import DataList
from tests.components.new_folder_popup import NewFolderPopup
from tests.components.delete_popup import DeletePopup
from tests.components.share_popup import SharePopup
from tests.components.auth_block import AuthBlock
from tests.components.copy_folder_popup import CopyFolderPopup

class CloudPage(Page):
    BASE_URL = 'https://cloud.mail.ru/home/'
    ERROR_MESSAGE = '//div[@class="notify-message"]'

    def __init__(self, driver, path):
        Page.__init__(self, driver)
        self.PATH = path

    @property
    def ad(self):
        return StartAd(self.driver)


    @property
    def copy_popup(self):
        return CopyFolderPopup(self.driver)

    @property
    def toolbars(self):
        return ToolBars(self.driver)

    @property
    def get_link_popup(self):
        return GetLinkPopup(self.driver)

    @property
    def datalist(self):
        return DataList(self.driver)

    @property
    def new_folder_popup(self):
        return NewFolderPopup(self.driver)

    @property
    def delete_popup(self):
        return DeletePopup(self.driver)

    @property
    def share_popup(self):
        return SharePopup(self.driver)

    @property
    def auth_block(self):
        return AuthBlock(self.driver)

    def error_notification_exists(self):
        try:
            self.wait(until=EC.presence_of_element_located((By.XPATH, self.ERROR_MESSAGE)))
        except exceptions.TimeoutException:
            return False
        return True
