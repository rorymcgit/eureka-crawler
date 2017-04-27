import urllib.request
from bs4 import BeautifulSoup
from crawler.db_translator import Translator

class Crawler():
    def __init__(self, translator = Translator()):
        # initializes an instance of the Translator class and assigns it to 'self'
        self.translator = translator
        # similar to Ruby's instance variables
        self.translator.set_environment()
        # calling Translator's set_environment method, which connects with the database

    def crawl(self, url):
        self.url = url
        # 'instance variable' action
        self.page = urllib.request.urlopen(url).read()
        # calls on the urllib library to open and read a webpage
        self.translator.write_url(url)
        # takes url from previous line, sends it to translator's write url method which then passes it on to the weburls table

    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        # setting the soup variable to a BS action.
        self.webpage_title = self.soup.title.string
        # sets variable to title string pulled from BS??
        self.translator.write_urls_and_titles(self.url, self.webpage_title)
        #sends url and title to translator method to then pass to database. 

# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
# crawler.return_content()
