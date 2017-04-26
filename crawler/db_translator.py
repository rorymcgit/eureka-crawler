import psycopg2


class Translator():
    def set_environment(self, db = "dbname=beetle_crawler_development"):
        self.database = psycopg2.connect(db)
        self.database_cursor = self.database.cursor()

    def write_url(self, url):
        self.database_cursor.execute("INSERT INTO weburls (weburl) VALUES (%s)",
                (url,))
