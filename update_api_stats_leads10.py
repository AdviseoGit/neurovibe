import re

def reorder_api_endpoints():
    with open('/data/workspace/projects/neurovibe/main.py', 'r') as f:
        content = f.read()

    # Den måste ligga FÖRE serve_html (catch-all) men nu ligger den uppenbarligen inte det 
    # med tanke på att den får 502 istället för 404 (vilket catch-all troligen gav)
    # Vänta, 502 betyder att appen kraschar eller timeoutar. Det betyder att vårt fel ligger någon annanstans.
    
    pass

if __name__ == "__main__":
    reorder_api_endpoints()
