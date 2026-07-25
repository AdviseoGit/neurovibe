import os
import re

resurser_path = "/data/workspace/projects/neurovibe/static/resurser.html"

if os.path.exists(resurser_path):
    with open(resurser_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_link = """
                    <a href="/inkluderande-kultur-npf.html" class="block group">
                        <div class="p-6 rounded-lg border border-white/5 hover:border-[#D83131]/50 transition-colors bg-white/[0.02]">
                            <div class="text-[#D83131] text-xs font-mono mb-3">Guide / För Chefer</div>
                            <h3 class="text-lg font-bold mb-2 group-hover:text-[#D83131] transition-colors">Bygg en inkluderande kultur för NPF</h3>
                            <p class="text-[#A0A0A0] text-sm leading-relaxed mb-4">Så skapar ni en arbetskultur där medarbetare med kognitiva profiler kan prestera på topp.</p>
                            <span class="text-sm font-semibold text-white group-hover:text-[#D83131] transition-colors">Läs guiden &rarr;</span>
                        </div>
                    </a>
"""
    
    if "inkluderande-kultur-npf.html" not in content:
        # insert after the first grid item in the second section (Arbetsmiljö & Chefer)
        pattern = r'(<h2 class="text-2xl font-bold mb-8">Arbetsmiljö & Chefer</h2>\s*<div class="grid md:grid-cols-2 gap-6">)'
        
        match = re.search(pattern, content)
        if match:
             content = content.replace(match.group(1), match.group(1) + new_link)
             with open(resurser_path, "w", encoding="utf-8") as f:
                 f.write(content)
             print("Resurser updated.")
        else:
            print("Could not find insertion point.")
    else:
        print("Link already exists in resurser.")
