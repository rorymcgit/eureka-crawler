import os
import sys
from crawler.crawler import Crawler

# Set Python's recursion depth limit (default is 1000)
# sys.setrecursionlimit(15000)

sites_to_crawl = "file://" + os.path.abspath("sites_to_crawl.html")

translator = Translator('postgresql://localhost/beetle_crawler_development', 5000)
crawler = Crawler(translator)
crawler.crawl(sites_to_crawl)
