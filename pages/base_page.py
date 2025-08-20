import allure
from playwright.async_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page


    async def visit(self, url: str):
        step = f'Opening the url "{url}"'
        with allure.step(step):
            await self.page.goto(url, wait_until='domcontentloaded')


