import urllib.request
import sys
from bs4 import BeautifulSoup
from crawler.db_translator import Translator


class Crawler():
    def __init__(self, translator = Translator()):
        sys.setrecursionlimit(10000)
        self.translator = translator

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
        self.webpage_title = self.find_webpage_title(soup)
        self.webpage_description = self.find_webpage_metadata(soup, 'description')
        self.webpage_keywords = self.find_webpage_metadata(soup, 'keywords')
        self.translator.write_urls_and_content(self.url, self.webpage_title, self.webpage_description, self.webpage_keywords)
        self.crawl_next_url()

    def save_found_weburls(self, soup):
        self.webpage_urls = []
        for link in soup.find_all('a', href=True):
            self.webpage_urls.append(link['href'])
        self.translator.prepare_urls_for_writing_to_db(self.webpage_urls)

    def crawl_next_url(self):
        next_url_to_crawl = self.translator.get_next_url()
        if self.translator.both_tables_are_not_full_yet():
            self.crawl(next_url_to_crawl)
        else:
            return self.translator.full_database_message()

    def find_webpage_title(self, soup):
        return soup.title.string if soup.title else ''

    def find_webpage_metadata(self, soup, name):
        try:
            return soup.find("meta", {"name": name})['content']
        except:
            return ''


# crawler = Crawler()
# crawler.crawl("http://www.makersacademy.com")
