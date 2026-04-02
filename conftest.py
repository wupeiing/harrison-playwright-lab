import pytest
from playwright.sync_api import sync_playwright
from src.pages.login_page import LoginPage


@pytest.fixture(scope="class")
def browser():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def page_with_login(page):
    login_page = LoginPage(page)

    login_page.visit()
    login_page.login("standard_user", "secret_sauce")

    yield page