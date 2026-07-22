import re

with open('/data/workspace/projects/neurovibe/static/resurser.html', 'r') as f:
    content = f.read()

# Add the new article to the resources page
new_card = """
                    <div class="bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow">
                        <div class="p-6">
                            <div class="text-sm font-medium text-indigo-600 mb-2">Guide (Augusti 2026)</div>
                            <h3 class="text-xl font-bold text-slate-900 mb-2"><a href="/post-semester-stress-npf.html" class="hover:text-indigo-600">Post-semester stress: Återgång till jobbet vid NPF</a></h3>
                            <p class="text-slate-600 mb-4 line-clamp-3">Så hanterar neurodivergenta medarbetare (ADHD/Autism) och chefer övergången tillbaka till jobbet efter semestern och undviker post-holiday burnout.</p>
                            <a href="/post-semester-stress-npf.html" class="text-indigo-600 font-medium hover:text-indigo-700">Läs guiden &rarr;</a>
                        </div>
                    </div>
"""

# Insert it before the first existing card in the grid
if "Post-semester stress: Återgång till jobbet vid NPF" not in content:
    grid_start = '<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">'
    parts = content.split(grid_start)
    
    if len(parts) == 2:
        new_content = parts[0] + grid_start + new_card + parts[1]
        with open('/data/workspace/projects/neurovibe/static/resurser.html', 'w') as f:
            f.write(new_content)
        print("Updated resurser.html")
    else:
        print("Could not find grid start")
else:
    print("Card already exists")
