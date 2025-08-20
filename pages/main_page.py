from playwright.async_api import Page
from components.main_page.top_menu_component import TopMenuComponent
from pages.base_page import BasePage


class MainPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.top_menu = TopMenuComponent(page)






