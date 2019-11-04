from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base_page import Page
from tests.components.start_ad import StartAd


class CloudMain(Page):
    BASE_URL = 'https://cloud.mail.ru/'

    @property
    def ad(self):
        return StartAd(self.driver)


