import scrapy


class QuotesSpider(scrapy.Spider):
    name = "follow_links"
    start_urls = [
        'https://quotes.toscrape.com/page/1/',
    ]

    def parse(self, response, **kwargs):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').get(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        # A shortcut for creating Requests
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse)
        # Mode 2 and more https://docs.scrapy.org/en/latest/intro/tutorial.html#following-links
        # for href in response.css('ul.pager a::attr(href)'):
        #     yield response.follow(href, callback=self.parse)
