class JDPage:
    def __init__(self, page):
        self.page = page
        self.search_term_input = page.locator(':nth-match([aria-label="搜索"], 1)')

    async def navigate(self):
        await self.page.goto("https://www.jd.com/")

    async def search(self, text):
        await self.search_term_input.fill(text)
        await self.search_term_input.press("Enter")
