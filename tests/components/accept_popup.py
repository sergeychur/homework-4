from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class AcceptPopup(Component):
    POPUP = '//div[@class="layer_sharing-mount"]'
    ACCEPT = './/button[@data-name="confirm"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))

    def accept(self):
        accept_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.ACCEPT)))
        accept_button.click()
        self.global_wait(EC.invisibility_of_element((By.XPATH, self.POPUP)))
