import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator

class Crawler():
    def __init__(self, translator = Translator()):
        self.translator = translator

    def crawl(self, url):
        self.url = url
        self.page = urllib.request.urlopen(url).read()
        self.translator.write_url(url)

    def return_all_content(self):
        soup = BeautifulSoup(self.page, "html.parser")
        self.save_found_weburls(soup)
        self.webpage_title = soup.title.string
        self.webpage_description = soup.find("meta", {"name":"description"})['content']
        self.webpage_keywords = soup.find("meta", {"name":"keywords"})['content']
        self.translator.write_urls_and_content(self.url, self.webpage_title, self.webpage_description, self.webpage_keywords)
        next_url_to_crawl = self.translator.get_next_url()
        # while self.translator.get_weburls_table_size()

    def save_found_weburls(self, soup):
        self.webpage_urls = []
        for link in soup.find_all('a', href=True):
            self.webpage_urls.append(link['href'])
        self.translator.prepare_urls_for_writing_to_db(self.webpage_urls)

# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
# crawler.return_all_content()
