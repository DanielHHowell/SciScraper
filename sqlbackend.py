import sqlite3

"""General flow
1. Connect to database
2. Create cursor
3. Execute action
4. Commit changes
5. Close connection 
"""

#conn = psycopg2.connect(dbname='database1' user='postgres' password='postgres123' host='localhost' port='5432')

def create_table():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS main")
    cur.execute("CREATE TABLE IF NOT EXISTS main (pmc TEXT, doi TEXT, title TEXT, authors TEXT, date TEXT)")
    conn.commit()
    conn.close()

def insert(pmc, doi, title, authors, date):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?)", (pmc, doi, title, authors, date))
    conn.commit()
    conn.close()

def view():
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM main")
    rows = cur.fetchall()
    conn.close()
    return rows


def delete(pmc):
    conn = sqlite3.connect("database.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM main WHERE pmc = ?", (pmc,))
    conn.commit()
    conn.close()
