import scrapy
from ..items import WordWithMeaningItem
import sqlite3
from sqlite3 import Error
import urllib.parse
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class EngtogeezSpider(scrapy.Spider):
    name = 'engtogeez'
    start_urls = ['https://www.geezexperience.com/']
    handle_httpstatus_list = [404]
    custom_settings = {
        'DUPEFILTER_DEBUG': True,
    }

    def __init__(self):
        self.create_connection()
        self.fetch_keywords()

    def parse(self, response):
        pass

    def create_connection(self):
        try:
            self.conn = sqlite3.connect('words.db')
            self.curr = self.conn.cursor()
        except Error as e:
            print(e)

    def fetch_keywords(self):
        self.curr.execute('select * from englishwords')
        self.words = self.curr.fetchall()
