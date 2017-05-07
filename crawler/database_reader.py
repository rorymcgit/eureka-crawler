import sqlalchemy
from sqlalchemy import create_engine, select, insert, MetaData, Table
from sqlalchemy.orm import sessionmaker


class DatabaseReader():
    def __init__(self, db = 'postgresql://localhost/eureka_development'):
        self.set_up_database(db)
        self.current_id = 1

    def set_up_database(self, db):
        database_engine = create_engine(db)
        self.connection = database_engine.connect()
        metadata = MetaData()
        self.weburls = Table('weburls', metadata, autoload = True, autoload_with = database_engine)

    def get_next_url(self):
        self.current_id += 1
        next_url_statement = select([self.weburls]).where(self.weburls.c.id == self.current_id)
        try:
            return self.connection.execute(next_url_statement).fetchone()['weburl']
        except TypeError:
            print(self.end_of_db_message())
        except KeyError:
            print(self.end_of_db_message())

    def get_weburls_table_size(self):
        select_all = select([self.weburls])
        return self.connection.execute(select_all).rowcount

    def url_is_in_database(self, url):
        select_statement = self.weburls.select(self.weburls.c.weburl == url)
        res_proxy = self.connection.execute(select_statement)
        results = [item[1] for item in res_proxy.fetchall()]
        return len(results)

    def end_of_db_message(self):
        return "No more web urls to crawl in the table."
