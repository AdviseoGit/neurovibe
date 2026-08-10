with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'r') as f:
    content = f.read()

content = content.replace('[ ] Lägg till lead capture-komponent tydligare "above the fold" på startsidan', '[x] Lägg till lead capture-komponent tydligare "above the fold" på startsidan')

with open('/data/workspace/projects/neurovibe/KAMPANJ.md', 'w') as f:
    f.write(content)
