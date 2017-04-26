import urllib.request
import psycopg2
from bs4 import BeautifulSoup

conn = psycopg2.connect("dbname=testpython")
cur = conn.cursor()

class Crawler():
    def crawl(self, url):
        print(url)
        self.page = urllib.request.urlopen(url).read()
        cur.execute("CREATE TABLE weburls (id serial PRIMARY KEY, url varchar);")
        cur.execute("INSERT INTO weburls (url) VALUES (%s)",
                (str(url)))
        conn.commit()
        cur.close()
        conn.close()
        #save url at this point to the db

    def return_content(self):
        self.soup = BeautifulSoup(self.page, "html.parser")
        self.webpage_title = self.soup.title.string

    # save url and self.webpage_title to another database table

# crawler = Crawler()
# crawler.crawl('https://www.webpagetest.org/')
