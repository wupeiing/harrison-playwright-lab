from src.lib.models import UserInfo
from src.pages.base_page import BasePage

class LoginPage(BasePage):

    def __init__(self, page):
        super().__init__(page)
        
        # --- [Section] Pre-Signup Locators ---
        self.signup_name_input = page.locator('input[data-qa="signup-name"]')
        self.signup_email_input = page.locator('input[data-qa="signup-email"]')
        self.signup_button = page.locator('button[data-qa="signup-button"]')

        # --- [Section] Enter Account Information ---
        self.title_mr_radio = page.locator('#id_gender1')
        self.title_mrs_radio = page.locator('#id_gender2')
        self.name_display_input = page.locator('input[data-qa="name"]') # 填寫資料頁的 Name
        self.email_display_input = page.locator('input[data-qa="email"]') # 唯讀的 Email
        self.password_input = page.locator('input[data-qa="password"]')
        
        # Date of Birth (Dropdowns)
        self.days_dropdown = page.locator('select[data-qa="days"]')
        self.months_dropdown = page.locator('select[data-qa="months"]')
        self.years_dropdown = page.locator('select[data-qa="years"]')

        # Newsletter & Offers (Checkboxes)
        self.newsletter_checkbox = page.locator('#newsletter')
        self.optin_checkbox = page.locator('#optin')

        # --- [Section] Address Information ---
        self.first_name_input = page.locator('input[data-qa="first_name"]')
        self.last_name_input = page.locator('input[data-qa="last_name"]')
        self.company_input = page.locator('input[data-qa="company"]')
        self.address1_input = page.locator('input[data-qa="address"]')
        self.address2_input = page.locator('input[data-qa="address2"]')
        self.country_dropdown = page.locator('select[data-qa="country"]')
        self.state_input = page.locator('input[data-qa="state"]')
        self.city_input = page.locator('input[data-qa="city"]')
        self.zipcode_input = page.locator('input[data-qa="zipcode"]')
        self.mobile_number_input = page.locator('input[data-qa="mobile_number"]')
        
        # Submit Button
        self.create_account_button = page.locator('button[data-qa="create-account"]')

    def signup_initial(self, username, password):
        self.signup_name_input.fill(username)
        self.signup_email_input.fill(password)
        self.signup_button.click()
    
    def detail_signup(self, user_info):
        # 填寫 Account Information
        if user_info.is_male:
            self.title_mr_radio.check()
        else:
            self.title_mrs_radio.check()

        # self.name_display_input.fill(user_info.name)
        # self.email_display_input.fill(user_info.email)  # 唯讀，通常不需要填寫
        self.password_input.fill(user_info.password)

        self.days_dropdown.select_option(user_info.dob_day)
        self.months_dropdown.select_option(user_info.dob_month)
        self.years_dropdown.select_option(user_info.dob_year)

        if user_info.newsletter:
            self.newsletter_checkbox.check()
        else:
            self.newsletter_checkbox.uncheck()

        if user_info.optin:
            self.optin_checkbox.check()
        else:
            self.optin_checkbox.uncheck()

        # 填寫 Address Information
        self.first_name_input.fill(user_info.first_name)
        self.last_name_input.fill(user_info.last_name)
        self.company_input.fill(user_info.company)
        self.address1_input.fill(user_info.address1)
        self.address2_input.fill(user_info.address2)
        self.country_dropdown.select_option(user_info.country)
        self.state_input.fill(user_info.state)
        self.city_input.fill(user_info.city)
        self.zipcode_input.fill(user_info.zipcode)
        self.mobile_number_input.fill(user_info.mobile_number)

        # 提交註冊表單
        self.create_account_button.click()
    