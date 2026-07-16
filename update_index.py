import re

with open('/data/workspace/projects/neurovibe/static/index.html', 'r') as f:
    html = f.read()

# Add link to post-semester guide in the resources section if it exists, otherwise just a general link
new_link = '''<a href="/post-semester-stress-npf.html" class="block bg-slate-800 p-6 rounded-lg border border-slate-700 hover:border-blue-500 transition-colors">
            <h3 class="text-xl font-semibold mb-2">Hantera Post-Semester Stress vid NPF</h3>
            <p class="text-gray-400 text-sm">Konkreta strategier för övergången tillbaka till arbetet för neurodivergenta och deras chefer.</p>
        </a>'''

if 'id="resurser"' in html and 'grid' in html.split('id="resurser"')[1][:500]:
    html = re.sub(r'(id="resurser".*?<div class="grid.*?>)', r'\1\n        ' + new_link, html, count=1, flags=re.DOTALL)
else:
    # Append to some section
    pass

with open('/data/workspace/projects/neurovibe/static/index.html', 'w') as f:
    f.write(html)
