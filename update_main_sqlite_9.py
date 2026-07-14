import re
with open('/data/workspace/projects/neurovibe/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_tool_usage = """async def save_tool_usage(data: ToolUsageData):
    os.makedirs("data", exist_ok=True)
    file_path = os.path.join("data", "tool_usage.csv")
    
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("timestamp,tool,modules,input_text,output_text,metadata\\n")
        
        import time
        import json
        timestamp = int(time.time())
        modules_str = json.dumps(data.modules) if data.modules else ""
        input_str = data.input_text.replace("\\n", " ").replace(",", ";") if data.input_text else ""
        output_str = data.output_text.replace("\\n", " ").replace(",", ";") if data.output_text else ""
        metadata_str = json.dumps(data.metadata) if data.metadata else ""
        
        f.write(f'{timestamp},{data.tool},"{modules_str}","{input_str}","{output_str}","{metadata_str}"\\n')
        
    return {"status": "success"}"""

new_tool_usage = """async def save_tool_usage(data: ToolUsageData):
    os.makedirs("data", exist_ok=True)
    import time
    import json
    import sqlite3
    import os
    
    timestamp = int(time.time())
    modules_str = json.dumps(data.modules) if data.modules else ""
    input_str = data.input_text.replace("\\n", " ").replace(",", ";") if data.input_text else ""
    output_str = data.output_text.replace("\\n", " ").replace(",", ";") if data.output_text else ""
    metadata_str = json.dumps(data.metadata) if data.metadata else ""
    
    # Save to SQLite
    try:
        db_path = os.path.join(os.path.dirname(__file__), "data", "neurovibe.db")
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(
            '''
            CREATE TABLE IF NOT EXISTS tool_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool TEXT NOT NULL,
                modules TEXT,
                input_text TEXT,
                output_text TEXT,
                metadata TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        cur.execute(
            "INSERT INTO tool_usage (tool, modules, input_text, output_text, metadata) VALUES (?, ?, ?, ?, ?)",
            (data.tool, modules_str, input_str, output_str, metadata_str)
        )
        conn.commit()
        conn.close()
        print(f"USAGE LOGGED (SQLite): {data.tool}")
    except Exception as e:
        print(f"SQLite Tool Usage Error: {e}")
        
    # Also save to CSV as fallback/legacy
    file_path = os.path.join("data", "tool_usage.csv")
    file_exists = os.path.isfile(file_path)
    try:
        with open(file_path, "a", encoding="utf-8") as f:
            if not file_exists:
                f.write("timestamp,tool,modules,input_text,output_text,metadata\\n")
            f.write(f'{timestamp},{data.tool},"{modules_str}","{input_str}","{output_str}","{metadata_str}"\\n')
    except Exception as e:
        print(f"CSV error: {e}")
        
    return {"status": "success"}"""

if old_tool_usage in content:
    content = content.replace(old_tool_usage, new_tool_usage)
    with open('/data/workspace/projects/neurovibe/main.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("main.py uppdaterad för att spara tool_usage i SQLite neurovibe.db")
else:
    print("Kunde fortfarande inte hitta en exakt matchning.")
