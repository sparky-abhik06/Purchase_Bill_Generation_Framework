import psycopg2
import logging


# Function to connect to the PostgreSQL database
class DatabaseConnection:
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def connect(self):
        try:
            conn = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            return conn
        except psycopg2.Error as e:
            logging.info("Unable to connect to the database: " + str(e))
            return None


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    db_connection = DatabaseConnection("postgres", "postgres", "password", "localhost", "5432").connect()
