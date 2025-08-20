import allure
from playwright.async_api import expect
from elements.base_element import BaseElement


class Button(BaseElement):

    @property
    def type_of(self) -> str:
        return "button"

    async def check_enabled(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is enabled'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_be_enabled()

    async def check_disabled(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is disabled'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_be_disabled()