import re
with open('/data/workspace/projects/neurovibe/main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We know new_tool_usage is in main.py from the cat output, let's just make sure it creates the right table structure
