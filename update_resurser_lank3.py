import os
import re

resurser_path = "/data/workspace/projects/neurovibe/static/resurser.html"

if os.path.exists(resurser_path):
    with open(resurser_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_link = """
                <!-- Guide: Kultur -->
                <a href="/inkluderande-kultur-npf.html" class="glass-panel p-8 border-white/10 hover:border-[#D83131] transition-all group flex flex-col h-full">
                    <div class="mb-4 text-xs font-mono text-[#D83131] tracking-widest uppercase">Guide</div>
                    <h2 class="text-xl font-bold text-white mb-3">Bygg en inkluderande kultur för NPF</h2>
                    <p class="text-[#808080] text-sm flex-grow">Så skapar ni en arbetskultur där medarbetare med kognitiva profiler kan prestera på topp.</p>
                </a>
"""
    
    if "inkluderande-kultur-npf.html" not in content:
        pattern = r'(<h2 class="text-xl font-bold text-white mb-3">Inkluderande Rekrytering</h2>\s*<p class="text-\[#808080\] text-sm flex-grow">Så anpassar du rekryteringsprocessen för kandidater med NPF för att inte missa dold talang.</p>\s*</a>)'
        
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
