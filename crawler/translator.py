import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table
from sqlalchemy.orm import sessionmaker
from crawler.url_checker import URLChecker
from crawler.url_splicer import URLSplicer

class Translator():
    def __init__(self,
                db = 'postgresql://localhost/beetle_crawler_development',
                database_limit = 1000,
                url_checker = URLChecker(),
                url_splicer = URLSplicer()):
        self.set_up_database(db)
        self.url_checker = url_checker
        self.url_splicer = url_splicer
        self.database_limit = database_limit
        self.current_id = 1

    def set_up_database(self, db):
        database_engine = create_engine(db)
        self.connection = database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with = database_engine)
        self.weburlsandcontent = Table('weburlsandcontent', metadata, autoload = True, autoload_with = database_engine)

    def write_url(self, url):
        if self.get_weburls_table_size() < self.database_limit:
            if self.url_checker.url_is_valid(url):
                url = self.url_splicer.cut_url(url)
                if not self.url_is_in_database(url):
                    statement = insert(self.weburls).values(weburl = url)
                    self.connection.execute(statement)
        else:
            return "Weburls table is full"

    def write_urls_and_content(self, page_metadata_dictionary):
        statement = insert(self.weburlsandcontent).values(
                        weburl = page_metadata_dictionary['url'],
                        title = page_metadata_dictionary['title'],
                        description = page_metadata_dictionary['description'],
                        keywords = page_metadata_dictionary['keywords'])
        self.connection.execute(statement)

    def prepare_urls_for_writing_to_db(self, weburls):
        for url in weburls:
            self.write_url(url)

    def get_next_url(self):
        self.current_id += 1
        next_url_statement = select([self.weburls]).where(self.weburls.c.id == self.current_id)
        try:
            return self.connection.execute(next_url_statement).fetchone()['weburl']
        except TypeError:
            print(self.end_of_db_message())

    def get_weburls_table_size(self):
        select_all = select([self.weburls])
        return self.connection.execute(select_all).rowcount

    def get_weburls_and_content_table_size(self):
        select_all = select([self.weburlsandcontent])
        return self.connection.execute(select_all).rowcount

    def url_is_in_database(self, url):
        select_statement = self.weburls.select(self.weburls.c.weburl == url)
        res_proxy = self.connection.execute(select_statement)
        results = [item[1] for item in res_proxy.fetchall()]
        return len(results)

    def end_of_db_message(self):
        return "No more web urls to crawl in the table."
