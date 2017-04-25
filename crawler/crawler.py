import requests

class Crawler():
    def crawl(self):
        self.page = requests.get("https://en.wikipedia.org/wiki")
