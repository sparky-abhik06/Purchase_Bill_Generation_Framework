import psycopg2
import logging
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv('DATABASE_URL')


# Function to connect to the PostgreSQL database
class DatabaseConnection:
    def __init__(self):
        # Neon.tech postgresql database connection string:
        self.db_url = database_url

    def connect(self):
        try:
            conn = psycopg2.connect(self.db_url)
            return conn
        except psycopg2.Error as e:
            logging.info("Unable to connect to the database: " + str(e))
            return None
