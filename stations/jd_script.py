from models.jd_model import JDPage
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=False)
        page = await browser.new_page()
        search_page = JDPage(page)
        await search_page.navigate()
        await search_page.search("口红")
        await page.wait_for_timeout(30000)
        await browser.close()


asyncio.run(main())
