import urllib.request
from crawler.database_writer import DatabaseWriter
from crawler.database_reader import DatabaseReader
from crawler.parser import Parser

class Crawler():
    def __init__(self, database_writer = DatabaseWriter(), database_reader = DatabaseReader(), parser = Parser()):
        self.database_writer = database_writer
        self.database_reader = database_reader
        self.parser = parser

    def crawl(self, url):
        self.url = url
        try:
            self.page = urllib.request.urlopen(url).read()
            self.database_writer.write_url(url)
            self.return_all_content()
        except urllib.error.HTTPError as err:
            print("Error: ", err.code)
            self.crawl_next_url()

    def return_all_content(self):
        self.save_found_weburls()
        page_metadata_dictionary = self.parser.create_soup_and_save_content(self.page)
        if page_metadata_dictionary:
            page_metadata_dictionary["url"] = self.url
            self.database_writer.write_urls_and_content(page_metadata_dictionary)
        self.crawl_next_url()

    def save_found_weburls(self):
        webpage_links = self.parser.create_soup_and_save_weburls(self.page)
        self.database_writer.prepare_urls_for_writing_to_db(webpage_links)

    def crawl_next_url(self):
        next_url_to_crawl = self.database_reader.get_next_url()
        # print("NEXT URL TO CRAWL: ", next_url_to_crawl)
        if next_url_to_crawl:
            self.crawl(next_url_to_crawl)
