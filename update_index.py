import re

file_path = '/data/workspace/projects/neurovibe/static/index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Add link to the new guide in the Resurser & Guider section
new_link = '''
                <a href="/arbetsplats-schema-npf.html" class="block p-6 bg-dark-800 border border-dark-700 rounded-lg hover:border-primary-500 transition-colors group">
                    <h3 class="text-xl font-bold mb-2 text-white group-hover:text-primary-500 transition-colors">Bygg ett hållbart schema vid NPF</h3>
                    <p class="text-gray-400 text-sm">Praktisk guide för att minska kognitiv belastning och kontextbyten. För HR, chefer och medarbetare.</p>
                </a>
'''

# Find the resources grid and insert the new link
insertion_point = content.find('<!-- Guider & Artiklar -->')
if insertion_point != -1:
    grid_start = content.find('<div class="grid grid-cols-1 md:grid-cols-2 gap-6 mt-8">', insertion_point)
    if grid_start != -1:
        insert_index = content.find('>', grid_start) + 1
        content = content[:insert_index] + new_link + content[insert_index:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated index.html")
