from src.lib.configs import BASE_URL
class BasePage:
    def __init__(self, page):
        self.page = page

    def visit_home_page(self):
        self.visit(BASE_URL)

    def visit(self, url):
        self.page.goto(url)