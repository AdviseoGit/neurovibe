import re

with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'r') as f:
    content = f.read()

new_content = re.sub(
    r'<title>Om Oss \| Neurovibe</title>',
    r'<title>Om Sajten | Neurovibe</title>',
    content
)

# Replace the specific title inside to "Om sajten"
new_content = re.sub(
    r'<h1 class="text-4xl font-bold tracking-tight text-white mb-6">Om Oss</h1>',
    r'<h1 class="text-4xl font-bold tracking-tight text-white mb-6">Om sajten</h1>',
    new_content
)

with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'w') as f:
    f.write(new_content)
