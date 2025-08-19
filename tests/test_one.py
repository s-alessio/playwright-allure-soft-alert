import pytest

from config import settings
from pages.main_page import MainPage



@pytest.mark.soft
async def test_example(main_page: MainPage):
    url = settings.get_base_url()
    await main_page.visit(url)

    await main_page.top_menu.logo_text.check_have_text("Playwright for Python111")
    await main_page.top_menu.docs_link.check_have_text("Docs111")
    await main_page.top_menu.api_link.check_have_text("API111")


