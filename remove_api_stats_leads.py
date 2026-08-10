import re

def remove_endpoint():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # The 502 error persists. It's possible the Railway instance is just down due to something else in main.py
    # Let's completely remove the endpoint we added, to see if the site comes back up.
    
    pattern = re.compile(r'@app\.get\("/api/stats/leads"\)[\s\S]*?(?=@app\.|$|if __name__)', re.MULTILINE)
    content = pattern.sub('', content)

    with open('/data/workspace/projects/neurovibe/main.py', 'w') as f:
        f.write(content)
    
    print("Removed /api/stats/leads to restore site uptime")

if __name__ == "__main__":
    remove_endpoint()
