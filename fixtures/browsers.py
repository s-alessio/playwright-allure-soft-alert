import re

import pytest
from playwright.async_api import async_playwright, Page
from _pytest.fixtures import SubRequest
from config import settings

def _sanitize(name: str) -> str:
    return re.sub(r'[^A-Za-z0-9._-]+', '_', name)

@pytest.fixture(params=settings.browsers)
async def browser_page(request: SubRequest) -> Page:
    async with async_playwright() as playwright:
        test_name = _sanitize(request.node.nodeid)
        browser_type = request.param

        browser = await playwright[browser_type].launch(headless=settings.headless)
        context = await browser.new_context(base_url=settings.get_base_url(),
                                  record_video_dir=settings.videos_dir)
        await context.tracing.start(screenshots=True, snapshots=True, sources=True)
        page = await context.new_page()

        yield page

        await context.tracing.stop(path=settings.tracing_dir.joinpath(f'{test_name}.zip'))
        video_path = await page.video.path()

        await context.close()
        await browser.close()

        request.node._allure_trace_zip = str(settings.tracing_dir.joinpath(f'{test_name}.zip'))
        request.node._allure_video_path = video_path


