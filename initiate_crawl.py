import os
import sys
from crawler.crawler import Crawler
from crawler.database_writer import DatabaseWriter

# Set Python's recursion depth limit (default is 1000)
sys.setrecursionlimit(15499)

sites_to_crawl = "file://" + os.path.abspath("sites_to_crawl.html")

database_writer = DatabaseWriter('postgresql://localhost/beetle_crawler_development', 10000)
crawler = Crawler(database_writer)
crawler.crawl(sites_to_crawl)
