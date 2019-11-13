from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions

from base_page import Page
from tests.components.invitation_list import InvitationList
from tests.components.accept_popup import AcceptPopup


class SharedPage(Page):
    BASE_URL = 'https://cloud.mail.ru/shared/incoming/'
    POPUP = '//div[contains(concat(\' \',@class,\' \'),\' b-layer__container_disko-popup \')]'
    AD = '//div[@class="share-promo"]'
    CLOSE_BUTTON = './/button[@data-name="close"]'

    def __init__(self, driver):
        Page.__init__(self, driver)

    @property
    def invitation_list(self):
        return InvitationList(self.driver)

    @property
    def accept_popup(self):
        return AcceptPopup(self.driver)

    def close_popup(self):
        try:
            self.wait(timeout=5, until=EC.presence_of_element_located((By.XPATH, self.POPUP)))
        except exceptions.TimeoutException:
            return
        else:
            ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        self.wait(EC.invisibility_of_element((By.XPATH, self.POPUP)))

    def close_ad(self):
        try:
            ad_div = self.wait(timeout=5, until=EC.presence_of_element_located((By.XPATH, self.AD)))
        except exceptions.TimeoutException:
            return
        else:
            close_button = self.wait(who=ad_div, until=EC.element_to_be_clickable((By.XPATH, self.CLOSE_BUTTON)))
            close_button.click()
        self.wait(EC.invisibility_of_element((By.XPATH, self.AD)))

    def close_annoying_adverts(self):
        self.close_popup()
        self.close_ad()
