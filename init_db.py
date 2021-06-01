import psycopg2


conn = psycopg2.connect('dbname=test')
cur = conn.cursor()


#import sqlite3

#connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    conn.executescript(f.read())

cur = conn.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()

