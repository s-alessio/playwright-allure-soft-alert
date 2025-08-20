import pytest
from playwright.async_api import Page
from pages.main_page import MainPage


@pytest.fixture()
async def main_page(browser_page: Page) -> MainPage:
    return MainPage(page=browser_page)
