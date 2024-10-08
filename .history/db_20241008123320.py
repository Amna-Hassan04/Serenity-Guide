import sqlite3

def init_db():
    conn = sqlite3.connect('peer_discussion.db')
    c = conn.cursor()
    c.execute('''
              CREATE TABLE IF NOT EXISTS comments
              (id INTEGER PRIMARY KEY, comment TEXT)
              ''')
    conn.commit()
    return conn, c

def insert_comment(conn, comment):
    c = conn.cursor()
    c.execute("INSERT INTO comments (comment) VALUES (?)", (comment,))
    conn.commit()

def fetch_comments(conn):
    c = conn.cursor()
    c.execute("SELECT comment FROM comments")
    return c.fetchall()

def close_db(conn):
    conn.close()
