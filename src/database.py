import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DB_PATH = os.path.join(BASE_DIR, "ids.db")


def connect():
    return sqlite3.connect(DB_PATH)


def create_table():   
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS detections(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        filename TEXT,

        total INTEGER,

        normal INTEGER,

        attack INTEGER,

        accuracy REAL,

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    conn.commit()
    conn.close()


def insert_detection(filename, total, normal, attack, accuracy):

    conn = connect()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO detections

        (filename,total,normal,attack,accuracy)

        VALUES(?,?,?,?,?)

    """, (filename, total, normal, attack, accuracy))

    conn.commit()

    conn.close()


def get_all():

    conn = connect()

    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()


    cursor.execute("""
        SELECT *
        FROM detections
        ORDER BY created_at DESC
    """)


    rows = cursor.fetchall()


    conn.close()


    return rows