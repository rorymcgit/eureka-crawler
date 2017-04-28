import psycopg2
import sqlalchemy

class Translator():
    #  CRUD actions with the database
    def set_environment(self, db = "dbname=beetle_crawler_development"):
        self.engine = create_engine(db)
    # def set_environment(self, db = "dbname=beetle_crawler_development"):
        # self.database = psycopg2.connect(db)
        # Initiates a connection to the database set in the parameter
        §
        # Allows Python code to execute PostgreSQL command in a database session

    def write_url(self, url):
        table.insert().values(name='foo')



    # def write_url(self, url):
        # self.database_cursor.execute("INSERT INTO weburls (weburl) VALUES (%s)",
        # # writes collected url to the weburls table in the database
        #         (url,))
        # self.database.commit()
        # Commits your changes in the database


    def write_urls_and_titles(self, url, title):
        self.database_cursor.execute("INSERT INTO weburlsandtitles (weburl, title) VALUES (%s, %s)",
                (url, title,))
        self.database.commit()
