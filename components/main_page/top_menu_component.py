from components.base_component import BaseComponent
from playwright.async_api import Page
from elements.image import Image
from elements.link import Link
from tools.routes import AppRoute

class TopMenuComponent(BaseComponent):

    def __init__(self, page: Page):
        super().__init__(page)

        self.top_nav_bar = self.page.locator("nav[aria-label='Main']")
        self.logo_text = Link(self.top_nav_bar,"a.navbar__brand b", "Logo text")
        self.docs_link = Link(self.top_nav_bar,f"a[href='{AppRoute.DOCS}']", "Docs link")
        self.api_link = Link(self.top_nav_bar, f"a[href='{AppRoute.API}']", "API link")


