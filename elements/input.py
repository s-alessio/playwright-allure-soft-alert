import allure
from playwright.async_api import Locator, expect
from elements.base_element import BaseElement

class Input(BaseElement):

    @property
    def type_of(self) -> str:
        return "input"

    async def fill(self, value: str, nth: int = 0, **kwargs):
        step=f'Fill {self.type_of} "{self.name}" to value "{value}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await locator.fill(value)

    async def select_value(self, value: str, nth: int = 0, **kwargs):
        step=f'Select in {self.type_of} "{self.name}" value "{value}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await locator.select_option(value)

    async def check_have_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" has a value "{value}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_have_value(value)

    async def get_value(self, nth: int = 0, **kwargs):
        step = f'Get value of {self.type_of} "{self.name}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            return await locator.input_value()

    async def check_selected_value(self, value: str, nth: int = 0, **kwargs):
        step = f'Checking that in {self.type_of} "{self.name}" selected value "{value}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_have_value(value)

