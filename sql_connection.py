import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()

def get_connection():
    connection= mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
    return connection

    # if 'connection' in locals() and connection.is_connected():
    #     cursor.close()
    #     connection.close()
    #     print("MySQL connection closed")