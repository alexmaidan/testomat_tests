from playwright.sync_api import expect


class ProjectsPage:
    def __init__(self,page):
        self.page = page

    def is_loaded(self):
        expect(self.page.locator(".common-flash-success")).to_be_visible()
        expect(self.page.locator(".common-flash-success")).to_have_text("Signed in successfully")

        expect(self.page.locator(".common-flash-success", has_text="Signed in successfully")).to_be_visible()