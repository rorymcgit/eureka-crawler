import psycopg2

class Translator():
    def set_environment(self, db = "dbname=beetle_crawler_development"):
        self.database = psycopg2.connect(db)
        self.database_cursor = self.database.cursor()

    def write_url(self, url):
        self.database_cursor.execute("INSERT INTO weburls (weburl) VALUES (%s)",
                (url,))
        self.database.commit()

    def write_urls_and_titles(self, url, title):
        self.database_cursor.execute("INSERT INTO weburlsandtitles (weburl, title) VALUES (%s, %s)",
                (url, title,))
        self.database.commit()

    def prepare_urls_for_writing_to_db(self, weburls_array):
        for url in weburls_array:
            self.write_url(url)
