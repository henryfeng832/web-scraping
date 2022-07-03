# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse, Request
from playwright.sync_api import sync_playwright

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from assist.cookies import get_cookies, set_cookies


class TaobaoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class TaobaoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def __init__(self):
        cookies_path = r'D:\workspaces\web-scraping\taobao\taobao\taobao.json'
        broswer = sync_playwright().start().chromium.launch(headless=False)
        page = broswer.new_page()
        js = """
            Object.defineProperties(navigator, {webdriver:{get:()=>undefined}});
            """
        page.add_init_script(js)
        page.context.add_cookies(get_cookies(cookies_path))
        page.wait_for_timeout(500)
        page.goto("https://login.taobao.com/member/login.jhtml?spm=a21bo.jianhua.754894437.1.5af911d9pG9a69&f=top&redirectURL=https%3A%2F%2Fwww.taobao.com%2F")
        page.wait_for_load_state('networkidle')
        if not page.locator("text=快速进入").is_visible():
            page.fill(selector="#fm-login-id", value="15999961458")
            page.fill(selector="#fm-login-password", value="wodetaobao321")
            page.click("#login-form > div.fm-btn > button")
            page.wait_for_load_state('networkidle')
            cookies = page.context.cookies()
            set_cookies(cookies, cookies_path)
        else:
            page.click("text=快速进入")
        page.wait_for_timeout(10000)
        self.broswer = broswer
        self.page = page

    def __del__(self):
        # self.broswer.close()
        print("================__del__====================")

    def process_request(self, request: Request, spider):
        print("================process_request====================")
        self.page.goto(request.url)
        self.page.wait_for_load_state("networkidle")
        return HtmlResponse(url=request.url, body=self.page.content(),
                            request=request, encoding='utf-8')

    def process_response(self, request, response: HtmlResponse, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
