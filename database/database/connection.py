# database/connection.py
import sqlite3
import os

# Абсолютный путь к базе данных
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'travel_agency.db'))

def get_connection():
    return sqlite3.connect(DB_PATH)
