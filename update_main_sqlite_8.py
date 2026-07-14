import re
with open('/data/workspace/projects/neurovibe/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Byta ut save_tool_usage som just nu loggar till CSV till att använda SQLite neurovibe.db
old_tool_usage = """async def save_tool_usage(data: ToolUsageData):
    file_path = os.path.join("data", "tool_usage.csv")
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["tool_name", "interaction_type", "timestamp"])
        writer.writerow([data.tool_name, data.interaction_type, datetime.now().isoformat()])
"""

new_tool_usage = """async def save_tool_usage(data: ToolUsageData):
    # Backward compat write to CSV (if anyone uses it), but MAIN storage is now SQLite
    file_path = os.path.join("data", "tool_usage.csv")
    file_exists = os.path.isfile(file_path)
    try:
        with open(file_path, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(["tool_name", "interaction_type", "timestamp"])
            writer.writerow([data.tool_name, data.interaction_type, datetime.now().isoformat()])
    except Exception as e:
        print(f"CSV error: {e}")

    try:
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_name TEXT NOT NULL,
                interaction_type TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        cur.execute(
            "INSERT INTO tool_usage (tool_name, interaction_type) VALUES (?, ?)",
            (data.tool_name, data.interaction_type)
        )
        conn.commit()
        conn.close()
        print(f"USAGE LOGGED (SQLite): {data.tool_name} - {data.interaction_type}")
    except Exception as e:
        print(f"SQLite Tool Usage Error: {e}")
"""

if old_tool_usage in content:
    content = content.replace(old_tool_usage, new_tool_usage)
    with open('/data/workspace/projects/neurovibe/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("main.py uppdaterad för att spara tool_usage i SQLite neurovibe.db")
else:
    print("Kunde inte hitta exakt matchning av save_tool_usage. Letar efter def save_tool_usage")
    if "def save_tool_usage" in content:
        print("Finns en annan version, uppdaterar inte automatiskt än.")
