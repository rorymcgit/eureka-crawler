import psycopg2

class Translator():
    def set_environment(self, db = "dbname=beetle_crawler_development"):
        self.database = psycopg2.connect(db)
        self.database_cursor = self.database.cursor()

    def write_url(self, url):
        self.database_cursor.execute("INSERT INTO weburls (weburl) VALUES (%s)",
                (url,))
        self.database.commit()

    def write_urls_and_content(self, url, title, description, keywords):
        self.database_cursor.execute("INSERT INTO weburlsandcontent (weburl, title, description, keywords) VALUES (%s, %s, %s, %s)",
                (url, title, description, keywords,))
        self.database.commit()

    def prepare_urls_for_writing_to_db(self, weburls_array):
        for url in weburls_array:
            if self.get_database_size() < 1000:
                self.write_url(url)
            else:
                raise Exception

    def get_database_size(self):
        self.database_cursor.execute("SELECT * FROM weburls;")
        return self.database_cursor.rowcount
