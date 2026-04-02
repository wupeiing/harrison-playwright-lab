import time
import logging

from src.pages.login_page import LoginPage
from src.pages.home_page import HomePage
from src.lib.utils import is_text_on_page, click_continue
from src.lib.models import UserInfo

logger = logging.getLogger(__name__)

class TestLogin:

    def test_signup_with_valid_information(self, page):

        user_info = UserInfo(
            is_male = True,
            name = "Test User3",
            email = "wupeiing3@gmail.com",
            password = "password123",
            first_name = "Test",
            last_name = "User",
            company = "Test Company",
            address1 = "123 Test St",
            address2 = "Apt 4",
            country = "United States",
            state = "California",
            city = "Test City",
            zipcode = "12345",
            mobile_number = "1234567890",
            dob_day = "1",
            dob_month = "January",
            dob_year = "1990",
            newsletter = True,
            optin = True
        )

        home_page = HomePage(page)
        home_page.visit_home_page()
        home_page.click_login_link()

        # Ensure New User signeup is there
        assert is_text_on_page(page, "New User Signup!"), "'New User Signup!' should be displayed"
        login_page = LoginPage(page)
        login_page.signup_initial(user_info.name, user_info.email)

        # Ensure 'Enter Account Information' is there after clicking Signup
        assert is_text_on_page(page, "Enter Account Information"), "'Enter Account Information' should be displayed"
        login_page.detail_signup(user_info)
        logger.info("All items are filled, now click continue button")

        # Ensure 'ACCOUNT CREATED!' is there after submitting the form
        assert is_text_on_page(page, "ACCOUNT CREATED!"), "'ACCOUNT CREATED!' should be displayed"
        click_continue(page)

        # Ensure user is logged in after finish the submitting
        assert is_text_on_page(page, f"Logged in as {user_info.name}"), f"'Logged in as {user_info.name}' should be displayed"
        home_page.click_delete_account_link()

        # Ensure 'ACCOUNT DELETED!' is there after deleting account
        assert is_text_on_page(page, "ACCOUNT DELETED!"), "'ACCOUNT DELETED!' should be displayed"
        click_continue(page)
