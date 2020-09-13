import scrapy
from ..items import MerriamWordCollectionItem


class WordsSpider(scrapy.Spider):
    name = 'words'
    base_url = 'https://www.merriam-webster.com/browse/thesaurus/'
    start_urls = [
        'https://www.merriam-webster.com/browse/thesaurus/e',
    ]
    letters = ['f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
               'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def parse(self, response):

        item = MerriamWordCollectionItem()
        word_list = response.css('.entries a::text').getall()
        for word in word_list:
            item['word'] = word
            yield item

        next_page = response.css('li.next a::attr(href)').get()
        if next_page != "javascript: void(0)":
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
        else:
            if len(self.letters) > 0:
                letter = self.letters.pop(0)
                next_page = self.base_url + letter
                yield scrapy.Request(next_page, callback=self.parse)
            else:
                print('---------------->   Finished all letters')
