import sqlite3

def check_db():
    conn = sqlite3.connect('/data/workspace/projects/neurovibe/data/neurovibe.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM neurovibe_leads")
    rows = cur.fetchall()
    print("Local DB content:")
    for row in rows:
        print(row)
    conn.close()

check_db()
