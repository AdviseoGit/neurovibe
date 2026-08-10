with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'r') as f:
    content = f.read()

content = content.replace('Löptid: pass 1 av 3', 'Löptid: pass 2 av 3')

with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'w') as f:
    f.write(content)
