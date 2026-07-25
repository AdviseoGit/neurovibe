import os
import re

resurser_path = "/data/workspace/projects/neurovibe/static/resurser.html"

if os.path.exists(resurser_path):
    with open(resurser_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_link = """
                <!-- Guide: Inkluderande Kultur -->
                <a href="/inkluderande-kultur-npf.html" class="block group">
                    <div class="h-full border border-white/10 bg-[#1A1A1A] p-8 rounded-xl hover:border-[#D83131] transition-colors relative overflow-hidden">
                        <div class="absolute top-0 right-0 p-4">
                            <span class="text-[10px] font-mono text-[#D83131] uppercase tracking-widest bg-[#D83131]/10 px-2 py-1 rounded">Guide</span>
                        </div>
                        <h2 class="text-xl font-bold text-white mb-3">Bygg en inkluderande kultur för NPF</h2>
                        <p class="text-[#A0A0A0] text-sm mb-6">Så skapar ni en arbetskultur där medarbetare med kognitiva profiler kan prestera på topp.</p>
                        <div class="flex items-center text-[#D83131] text-sm font-bold">
                            <span>Läs guiden</span>
                            <span class="ml-2 group-hover:translate-x-1 transition-transform">→</span>
                        </div>
                    </div>
                </a>
"""
    
    if "inkluderande-kultur-npf.html" not in content:
        # insert after Inkluderande Rekrytering
        pattern = r'(<h2 class="text-xl font-bold text-white mb-3">Inkluderande Rekrytering</h2>\s*<p class="text-\[#A0A0A0\] text-sm mb-6">Hur man undviker neurotypiska bias i anställningsprocessen.</p>\s*<div class="flex items-center text-\[#D83131\] text-sm font-bold">\s*<span>Läs guiden</span>\s*<span class="ml-2 group-hover:translate-x-1 transition-transform">→</span>\s*</div>\s*</div>\s*</a>)'
        
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
