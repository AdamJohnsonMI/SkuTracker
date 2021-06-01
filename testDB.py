import psycopg2



conn = psycopg2.connect("dbname='posts' user='adam' host='localhost' password='adamm1'")
cur = conn.cursor()

cur.execute('SELECT * from posts')

results = cur.fetchall()

for result in results:
    print(result)