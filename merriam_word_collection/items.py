import scrapy


class MerriamWordCollectionItem(scrapy.Item):
    word = scrapy.Field()


class WordWithMeaningItem(scrapy.Item):
    word = scrapy.Field()
    wordtype = scrapy.Field()
    meanings = scrapy.Field()
    examples = scrapy.Field()
    moreexamples = scrapy.Field()
    synonyms = scrapy.Field()
    antonyms = scrapy.Field()


class EngtoTigItem(scrapy.Item):
    keyword = scrapy.Field()
