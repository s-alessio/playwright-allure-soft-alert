from playwright.async_api import Page
import logging


class BaseComponent:
    def __init__(self, page: Page):
        self.page = page

