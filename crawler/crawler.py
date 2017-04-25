import requests

class Crawler():
    def crawl(self):
        page = requests.get("https://en.wikipedia.org/wiki")
        return page.status_code
