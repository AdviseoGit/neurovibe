import sqlite3
import json

db_path = "/data/workspace/projects/neurovibe/data/neurovibe.db"
try:
    conn = sqlite3.connect(db_path)
    print("Tables:", conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall())
    print("\nColumns in tool_usage:")
    for col in conn.execute("PRAGMA table_info(tool_usage)").fetchall():
        print(col)
except Exception as e:
    print(e)
