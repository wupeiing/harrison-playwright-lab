
from src.pages.base_page import BasePage

class HomePage(BasePage):

    LOGIN_LINK = 'a[href="/login"]'
    DELETE_ACCOUNT_LINK = 'a[href="/delete_account"]'
    
    def click_login_link(self):
        login_btn = self.page.locator(self.LOGIN_LINK)
        login_btn.wait_for(state="visible", timeout = 5000)
        login_btn.click()

    def click_delete_account_link(self):
        delete_account_btn = self.page.locator(self.DELETE_ACCOUNT_LINK)
        delete_account_btn.wait_for(state="visible", timeout=5000)
        delete_account_btn.click()