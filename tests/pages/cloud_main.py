from base_page import Page
from tests.components.start_ad import StartAd
from tests.components.toolbars import ToolBars
from tests.components.get_link_popup import GetLinkPopup
from tests.components.datalist import DataList
from tests.components.new_folder_popup import NewFolderPopup
from tests.components.delete_popup import DeletePopup


class CloudMain(Page):
    BASE_URL = 'https://cloud.mail.ru/'

    @property
    def ad(self):
        return StartAd(self.driver)

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


