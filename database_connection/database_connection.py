import psycopg2
import logging


# Function to connect to the PostgreSQL database
class DatabaseConnection:
    def __init__(self):
        # Neon.tech postgresql database connection string:
        self.db_url = "postgresql://texas_db_owner:Z09LBvPoEzRb@ep-restless-mouse-a151ytfv.ap-southeast-1.aws.neon.tech/texas_db?sslmode=require"

    def connect(self):
        try:
            conn = psycopg2.connect(self.db_url)
            return conn
        except psycopg2.Error as e:
            logging.info("Unable to connect to the database: " + str(e))
            return None
