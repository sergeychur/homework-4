from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from base_page import Page


class Account(Page):
    BASE_URL = 'https://account.mail.ru/'
    PATH = 'login'
    LOGIN = '//input[@name="Login"]'
    PASSWORD = '//input[@name="Password"]'
    NEXT = '//button[@data-test-id="next-button"]'
    SUBMIT = '//button[@data-test-id="submit-button"]'

    def set_login(self, login):
        login_field = self.wait(EC.element_to_be_clickable((By.XPATH, self.LOGIN)))
        login_field.click()
        login_field.send_keys(login)

    def set_password(self, password):
        password_field = self.wait(EC.element_to_be_clickable((By.XPATH, self.PASSWORD)))
        password_field.click()
        password_field.send_keys(password)

    def go_next(self):
        next_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.NEXT)))
        next_button.click()

    def submit(self):
        submit_button = self.wait(EC.element_to_be_clickable((By.XPATH, self.SUBMIT)))
        submit_button.click()

    def login(self, login, password, redirect=None):
        if redirect is not None:
            self.PATH += '?success_redirect={}'.format(redirect)
        self.open()
        self.set_login(login)
        self.go_next()
        self.set_password(password)
        self.submit()
        if redirect is not None:
            self.wait(EC.url_matches(redirect))
