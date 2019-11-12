from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class AuthBlock(Component):
    AUTH_BLOCK = '//table[@class="x-ph__auth"]'
    LOGOUT_HREF = './/a[@id="PH_logoutLink"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.AUTH_BLOCK)))

    def logout(self):
        logout_href = self.wait(EC.element_to_be_clickable((By.XPATH, self.LOGOUT_HREF)))
        prev = self.driver.current_url
        logout_href.click()
        self.global_wait(EC.url_changes(url=prev))

