import traceback
from typing import Union

import allure
from playwright.async_api import Locator, FrameLocator, expect
from tools import soft_allure


class BaseElement:
    def __init__(self, root: Union[Locator, FrameLocator], locator: str, name: str):
        """

        :param root: - part of webpage (Frame, for example) in which the locator is searched . If the locator is searched over all webpage root can be set to page.locator("body")
        :param locator: - locator of element
        :param name: name of element
        """
        self.root = root
        self.name = name
        self.locator = locator

    @property
    def type_of(self) -> str:
        return "base element"

    async def get_locator(self, nth: int = 0, **kwargs) -> Locator:
        locator = self.locator.format(**kwargs)
        step = f'Getting locator with "{locator}" at index "{nth}"'
        with allure.step(step):
            return self.root.locator(locator).nth(nth)

    async def check_have_text(self, text: str, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} of "{self.name}" has text "{text}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            try:
                locator_text = (await locator.inner_text()).strip()
                assert locator_text == text, f"Expected text «{text}», found: «{locator_text}», for locator {locator}"
            except AssertionError as e:
                if soft_allure.safe_assert:
                    msg = f"{step}: {e}"
                    soft_allure.safe_errors.append(msg)
                    soft_allure.attach_text_to_failed_step(str(e), attach_name="Soft assertion")
                else:
                    raise
            except Exception:
                raise

    async def check_visible(self, nth: int = 0, **kwargs):
        step = f'Checking that {self.type_of} "{self.name}" is visible'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await expect(locator).to_be_visible()

    async def click(self, nth: int = 0, **kwargs):
        step = f'Clicking {self.type_of} "{self.name}"'
        with allure.step(step):
            locator = await self.get_locator(nth, **kwargs)
            await locator.click()
