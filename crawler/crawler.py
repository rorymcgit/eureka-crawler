import urllib.request
import sys
import os
from crawler.db_translator import Translator
from crawler.parser import Parser

class Crawler():
    def __init__(self, translator = Translator(), parser = Parser()):
        sys.setrecursionlimit(10000)
        self.translator = translator
        self.parser = parser

    def crawl(self, url):
        self.url = url
        try:
            self.page = urllib.request.urlopen(url).read()
            self.translator.write_url(url)
            self.return_all_content()
        except urllib.error.HTTPError as err:
            print("Error: ", err.code)
            self.crawl_next_url()

    def return_all_content(self):
        self.save_found_weburls()
        page_metadata_dictionary = self.parser.create_soup_and_save_content(self.page)
        if page_metadata_dictionary:
            page_metadata_dictionary["url"] = self.url
            self.translator.write_urls_and_content(page_metadata_dictionary)
            self.crawl_next_url()
        else:
            self.crawl_next_url()

    def save_found_weburls(self):
        webpage_links = self.parser.create_soup_and_save_weburls(self.page)
        self.translator.prepare_urls_for_writing_to_db(webpage_links)

    def crawl_next_url(self):
        next_url_to_crawl = self.translator.get_next_url()
        # print("NEXT URL TO CRAWL: ", next_url_to_crawl)
        if next_url_to_crawl:
            self.crawl(next_url_to_crawl)


# sites_to_crawl = "file://" + os.path.abspath("no_content.html")

# crawler = Crawler()
# crawler.crawl("http://www.makersacademy.com")
