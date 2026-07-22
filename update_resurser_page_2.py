import re

with open('/data/workspace/projects/neurovibe/static/resurser.html', 'r') as f:
    content = f.read()

# Add the new article to the resources page
new_card = """
                <!-- Ny Artikel -->
                <div class="resource-card bg-white rounded-xl shadow-sm border border-slate-200 overflow-hidden hover:shadow-md transition-shadow flex flex-col h-full filter-item" data-category="guider">
                    <div class="h-48 bg-slate-100 flex items-center justify-center p-6 border-b border-slate-200">
                        <svg class="w-16 h-16 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                        </svg>
                    </div>
                    <div class="p-6 flex flex-col flex-grow">
                        <div class="flex items-center justify-between mb-2">
                            <span class="text-xs font-bold uppercase tracking-wider text-indigo-600">Guide</span>
                            <span class="text-xs text-slate-500">Aug 2026</span>
                        </div>
                        <h3 class="text-xl font-bold text-slate-900 mb-2">Återgång till arbetet: Post-semester stress</h3>
                        <p class="text-slate-600 mb-6 flex-grow text-sm">Så hanterar neurodivergenta medarbetare (ADHD/Autism) och chefer övergången tillbaka till jobbet efter semestern och undviker post-holiday burnout.</p>
                        <a href="/post-semester-stress-npf.html" class="inline-flex items-center text-indigo-600 font-medium hover:text-indigo-700">
                            Läs guiden <span aria-hidden="true" class="ml-1">&rarr;</span>
                        </a>
                    </div>
                </div>
"""

grid_start = '<div id="resourcesContainer" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">'
if "Återgång till arbetet: Post-semester stress" not in content:
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
