
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import sqlite3
from sqlite3 import Error
from merriam_word_collection.items import MerriamWordCollectionItem


class MerriamWordCollectionPipeline:

    def __init__(self):
        self.create_connection()
        self.create_table()

    def create_connection(self):
        try:
            self.conn = sqlite3.connect('merriam_dictionary.db')
            self.curr = self.conn.cursor()
        except Error as e:
            print(e)

    def create_table(self):
        try:
            self.curr.execute('''CREATE TABLE IF NOT EXISTS dictionary
                                (word text, wordtype text,
                                 meanings text,
                                 examples text, 
                                 moreexamples text, 
                                 synonyms text,
                                 antonyms text)''')
        except Error as e:
            print(e)

    def store_word_definition(self, item):
        try:
            self.curr.execute(
                ' INSERT INTO dictionary VALUES (?,?,?,?,?,?,?) ',
                (item['word'],
                 item['wordtype'],
                 item['meanings'],
                 item['examples'],
                 item['moreexamples'],
                 item['synonyms'],
                 item['antonyms']))
            self.conn.commit()
        except Error as e:
            print(e)

    def store_verb_endings(self, item):
        try:
            self.curr.execute(
                ' INSERT INTO dictionary VALUES (?,?,?,?) ', (item['word'], item['wordtype'], item['meanings'], item['examples']))
            self.conn.commit()
        except Error as e:
            print(e)
        pass

    def process_item(self, item, spider):
        self.store_word_definition(item)
        return item

        # adapter = ItemAdapter(item)
        # if adapter['word'] in self.ids_seen:
        #     self.store_verb_endings(item)
        #     raise DropItem("Duplicate item found: %r" % item['word'])
        #     pass
        # else:
        #     self.ids_seen.add(adapter['word'])
        #     self.store_word_definition(item)
        #     return item

        # Code for words spider
        # def __init__(self):
        #     self.create_connection()
        #     self.create_table()

        # def create_connection(self):
        #     try:
        #         self.conn = sqlite3.connect('words_exercise.db')
        #         self.curr = self.conn.cursor()
        #         print('Connected to database')
        #     except Error as e:
        #         print(e)

        # def create_table(self):
        #     try:
        #         self.curr.execute('''CREATE TABLE IF NOT EXISTS englishwords
        #                             (engword text)''')
        #         print('Table created')
        #     except Error as e:
        #         print(e)

        # def store_data(self, item):
        #     try:
        #         self.curr.execute(
        #             ' INSERT INTO englishwords VALUES (?) ', (item['word'],))
        #         self.conn.commit()
        #     except Error as e:
        #         print(e)

        # def process_item(self, item, spider):
        #     # self.store_data(item)
        #     return item
