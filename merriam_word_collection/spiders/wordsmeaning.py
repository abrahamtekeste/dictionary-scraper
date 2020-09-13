import scrapy
from ..items import WordWithMeaningItem
import sqlite3
from sqlite3 import Error
import urllib.parse
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError


class WordsmeaningSpider(scrapy.Spider):
    name = 'wordsmeaning'
    start_urls = ['https://www.merriam-webster.com/dictionary/a']
    handle_httpstatus_list = [404, 301, 302]

    custom_settings = {
        'DUPEFILTER_DEBUG': True,
    }

    def __init__(self):
        self.create_connection()
        self.fetch_keywords()

    def parse(self, response):
        base_url = 'https://www.merriam-webster.com/dictionary/'

        item = WordWithMeaningItem()

        if (not response.css('.mispelled-word')):
            item['word'] = urllib.parse.unquote(
                response.request.url.rsplit('/')[-1])
            item['wordtype'] = response.css('span.fl a::text').get()
            item['meanings'] = self.clean_meanings(response)
            item['examples'] = self.clean_examples(response)
            item['moreexamples'] = self.clean_more_examples(response)
            item['synonyms'] = self.clean_synonyms(response)
            item['antonyms'] = self.clean_antonyms(response)

            yield item

        if (len(self.words) > 0):
            next_page = base_url + urllib.parse.quote(self.words.pop(0)[0])
            yield scrapy.Request(next_page, callback=self.parse)

    def create_connection(self):
        try:
            self.conn = sqlite3.connect('words.db')
            self.curr = self.conn.cursor()
        except Error as e:
            print(e)

    def fetch_keywords(self):
        self.curr.execute('select * from englishwords limit 50')
        self.words = self.curr.fetchall()

    def clean_meanings(self, response):
        meanings = ""
        for container in response.css('div.vg'):
            for meaning in container.css('span.dt span.dtText'):
                meanings = meanings + \
                    "".join(meaning.css('::text').getall()) + '|\n'
        return meanings

    def clean_examples(self, response):
        examples = ""
        for i in range(len(response.css('.in-sentences span.ex-sent').extract())):
            examples = examples + \
                "".join(response.css('.in-sentences span.ex-sent')
                        [i].css('.t *::text').extract()) + '|\n'
        return examples

    def clean_more_examples(self, response):
        examples = ""
        for i in range(len(response.css('.on-web span.ex-sent').extract())):
            examples = examples + "".join(response.css('.on-web span.ex-sent')
                                          [i].css('.t *::text').extract()) + "|\n"
        return examples

    def clean_synonyms(self, response):
        synonyms = ""
        i = 0
        p = response.xpath('//div[@id="synonyms-anchor"]/p')
        while (i < len(p)):
            if (re.search("Synonyms", p[i].css('p::text').get())):
                # synonyms = synonyms + '\n' + p[i].css('p::text').get() + '\n'
                synonyms = synonyms + ",\n".join(response.xpath(
                    '//div[@id="synonyms-anchor"]/ul[{}]/li/a/text()'.format(i+1)).getall()) + ',\n'
            i += 1
        return synonyms

    def clean_antonyms(self, response):
        antonyms = ""
        i = 0
        p = response.xpath('//div[@id="synonyms-anchor"]/p')
        while (i < len(p)):
            if (re.search("Antonyms", p[i].css('p::text').get())):
                # antonyms = antonyms + p[i].css('p::text').get() + '\n'
                antonyms = antonyms + ",\n".join(response.xpath(
                    '//div[@id="synonyms-anchor"]/ul[{}]/li/a/text()'.format(i+1)).getall()) + ',\n'
            i += 1
        return antonyms
