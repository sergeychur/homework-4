from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from tests.components.component import Component


class InvitationList(Component):
    DATALIST_DIV = '//div[@id="datalist"]'
    # was before : datalist-item_type-invite
    NEEDED_FILE_DIV = './/div[contains(concat(\' \',@class,\' \'),\' ' \
                      'b-collection__item_datalist-mode-shared-incoming \')' \
                      ' and .//span[contains(., {})]]'
    # the strange thing above is needed because there us no usable data-id or data-name or whatever attribute
    # we have to take div which contains span with text such as the name of folder we are looking for
    ACCEPT_LINK = './/span[@class="b-filename__name"]'
    SHARE_BUTTON = '//button[contains(concat(\' \',@class,\' \'),\' btn_publish \')]'

    def __init__(self, driver):
        Component.__init__(self, driver=driver)
        self.root = self.wait(EC.presence_of_element_located((By.XPATH, self.DATALIST_DIV)))

    def accept_by_name(self, name):
        needed_file = self.wait(EC.presence_of_element_located(locator=(By.XPATH, self.NEEDED_FILE_DIV.format(name))))
        link = self.wait(who=needed_file, until=EC.element_to_be_clickable(locator=(By.XPATH, self.ACCEPT_LINK)))
        link.click()

    def wait_till_accepted(self, name):
        needed_file = self.wait(EC.presence_of_element_located(locator=(By.XPATH, self.NEEDED_FILE_DIV.format(name))))
        self.wait(who=needed_file, until=EC.element_to_be_clickable(locator=(By.XPATH, self.SHARE_BUTTON)))
