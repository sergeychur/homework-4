from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


from component import Component


class StartAd(Component):
    CLOSE_BUTTON = '//*[@class="Dialog__close--1rKyk"]'

    def close(self):
        close_button = self.wait(EC.presence_of_element_located((By.XPATH, self.CLOSE_BUTTON)))
        close_button.click()
