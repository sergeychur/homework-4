# coding=utf-8
from time import sleep

from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from tests.components.component import Component


class HistoryPopup(Component):
    POPUP = '//div[@data-bem="b-file-history"]'
    HISTORY_ROW = '//div[contains(@class,"datalist-item datalist-item_file-version")]'
    CLOSE_BTN = '//div[@class="b-file-history__controls"]//button[@data-name="close"][@class="btn "]'
    LAST_RECOVERY_COL = '//div[@class="datalist-item__col datalist-item__col_file-version-recovery-options datalist-item__col_file-version datalist-item__col_file-version-last"]'
    REWRITE_BTN = '//a[@data-num="0"][@data-name="rewrite"]'
    ACCEPT_BTN = '//button[@data-name="accept"][@data-bem="btn"]'
    PAID_FEATURE_MSG = '//div[@class="b-paid-feature__file-history-inner"]'
    WAIT_SPINNER = '//div[@class="b-file-history__waiting"]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.POPUP)))
        _ = self.wait(EC.invisibility_of_element_located((By.XPATH, self.WAIT_SPINNER)))

    def get_history_list(self):
        items_rows_number = len(self.driver.find_elements(By.XPATH, self.HISTORY_ROW))

        result = []
        for i in range(1, items_rows_number + 1):
            row = self.driver.find_element(By.XPATH, '({})[{}]'.format(self.HISTORY_ROW, i)).text
            result.append(row)
        return result

    def close(self):
        close = self.wait(EC.element_to_be_clickable((By.XPATH, self.CLOSE_BTN)))
        ActionChains(self.driver).move_to_element(close).click().perform()
        self.global_wait(EC.invisibility_of_element((By.XPATH, self.POPUP)))

    def replace_with_last(self):
        action_chains = ActionChains(self.driver)
        recovery_col = self.driver.find_element(By.XPATH, self.LAST_RECOVERY_COL)
        action_chains.move_to_element(recovery_col).perform()
        action_chains.move_by_offset(0, 20).click().perform()
        WebDriverWait(self.driver, 10)
        accept_btn = self.driver.find_element(By.XPATH, self.ACCEPT_BTN)
        # accept_btn = self.wait(EC.element_to_be_clickable((By.XPATH, self.ACCEPT_BTN)), timeout=30)
        # accept_btn.click()
        action_chains.move_to_element(accept_btn).click().perform()

    def is_replacing_allowed(self):
        try:
            self.wait(EC.presence_of_element_located((By.XPATH, self.PAID_FEATURE_MSG)))
            return False
        except TimeoutException:
            return True
