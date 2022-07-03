# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import openpyxl
import psycopg2


class DoubanMoviceTop250ByExcel:
    def __init__(self):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Top250"
        ws.append(("标题", "评分", "主题", "时长", "简介", "链接"))
        self.wb = wb
        self.ws = ws

    def close_spider(self, spider):
        self.wb.save("豆瓣电影数据表.xlsx")

    def process_item(self, item, spider):
        title = item.get("title", "")
        rank = item.get("rank", "")
        subject = item.get("subject", "")
        duration = item.get("duration", "")
        introduction = item.get("introduction", "")
        link = item.get("link", "")
        self.ws.append((title, rank, subject, duration, introduction, link))
        return item


class DoubanMoviceTop250ByDB:
    def __init__(self):
        self.conn = psycopg2.connect(database="douban", user="postgres", password="postgrespw", host="127.0.0.1", port="49153")
        self.cur = self.conn.cursor()
        self.data = []

    def close_spider(self, spider):
        if len(self.data) > 0:
            self._write_to_db()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get("title", "")
        rank = item.get("rank", "")
        subject = item.get("subject", "")
        duration = item.get("duration", "")
        introduction = item.get("introduction", "")
        link = item.get("link", "")
        self.data.append((title, rank, subject, duration, introduction, link))
        if len(self.data) >= 100:
            self._write_to_db()
            self.data.clear()
        return item

    def _write_to_db(self):
        self.cur.executemany(
            'insert into top250 (title, rank, subject, duration, introduction, link) values (%s, %s, %s, %s, %s, %s)',
            self.data
        )
        self.conn.commit()
