import scrapy

from ..items import DoubanTop250Item


class Doubantop250Spider(scrapy.Spider):
    name = 'doubantop250'
    allowed_domains = ['movie.douban.com']

    def start_requests(self):
        for pageno in range(10):
            yield scrapy.Request(url=f'http://movie.douban.com/top250?start={pageno * 25}&filter=')

    def parse(self, response, **kwargs):
        for item in response.css('#content > div > div.article > ol > li'):
            movice_item = {
                "rank": item.css('span.rating_num::text').get(),
                "title": item.css('div.info > div.hd > a > span:nth-child(1)::text').get(),
                "subject": item.css('div.info > div.bd > p.quote > span.inq::text').get(),
                "link": item.css('div.info > div.hd > a::attr(href)').get()
            }
            yield scrapy.Request(
                url=item.css('div.info > div.hd > a::attr(href)').get(),
                callback=self.parse_detail,
                cb_kwargs={"item": movice_item}
            )

    def parse_detail(self, response, **kwargs):
        movice_item = kwargs.get('item')
        sel = scrapy.Selector(response)
        movice_item['duration'] = sel.css('span[property="v:runtime"]::attr(content)').get()
        movice_item['introduction'] = sel.css('span[property="v:summary"]::text').get().strip()
        yield movice_item
