import os

import mysql.connector
from dotenv import load_dotenv


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME")
}


def get_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection


if __name__ == "__main__":
    connection = get_connection()
    print("MySQL connection successful!")
    connection.close()