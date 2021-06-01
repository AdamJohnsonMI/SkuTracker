DROP TABLE IF EXISTS posts;

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);



CREATE TABLE posts (
    id SERIAL PRIMARY KEY ,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);

CREATE USER readonly  WITH ENCRYPTED PASSWORD 'readonly';
GRANT USAGE ON SCHEMA public to adam;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO adam;

-- repeat code below for each database:

GRANT CONNECT ON DATABASE postings to adam;
\c foo
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO adam; --- this grants privileges on new tables generated in new database "foo"
GRANT USAGE ON SCHEMA public to adam; 
GRANT SELECT ON ALL SEQUENCES IN SCHEMA public TO adam;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO adam;


cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute('SELECT * FROM posts');
    posts = cursor.fetchall()