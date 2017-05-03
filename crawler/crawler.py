import urllib.request
import sys
import os
from bs4 import BeautifulSoup
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
        except:
            self.crawl_next_url()

    def return_all_content(self):
        soup = BeautifulSoup(self.page, "html.parser", from_encoding="UTF-8")
        self.save_found_weburls(soup)
        page_metadata_dictionary = self.parser.create_soup_and_save_content(self.page)
        if page_metadata_dictionary:
            page_metadata_dictionary["url"] = self.url
            self.translator.write_urls_and_content(page_metadata_dictionary)
            self.crawl_next_url()
        else:
            self.crawl_next_url()

    def save_found_weburls(self, soup):
        self.webpage_urls = []
        for link in soup.find_all('a', href=True):
            self.webpage_urls.append(link['href'])
        self.translator.prepare_urls_for_writing_to_db(self.webpage_urls)

    def crawl_next_url(self):
        next_url_to_crawl = self.translator.get_next_url()
        # print("NEXT URL TO CRAWL: ", next_url_to_crawl)
        if self.translator.both_tables_are_not_full_yet():
            if next_url_to_crawl != None:
                self.crawl(next_url_to_crawl)
        else:
            return self.translator.full_database_message()


# sites_to_crawl = "file://" + os.path.abspath("no_content.html")

# crawler = Crawler()
# crawler.crawl(sites_to_crawl)
