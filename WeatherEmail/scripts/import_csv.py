import csv, sqlite3

import pandas as pandas

conn = sqlite3.connect("../db.sqlite3")
cursor = conn.cursor()

with open('top_100_cities.csv', 'r', encoding='utf-8', errors='ignore') as file:
    delim = csv.DictReader(file)
    to_db = [(i['City'], i['State']) for i in delim]

cursor.executemany("INSERT INTO newsletter_cities (city, state) VALUES (?, ?);", to_db)
conn.commit()
conn.close()
