import re
import os

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'r') as f:
    content = f.read()

nav_html = """
    <!-- Navigation -->
    <nav class="p-6 relative z-10">
        <div class="max-w-7xl mx-auto flex justify-between items-center">
            <a href="/" class="text-2xl font-bold tracking-tighter text-white hover:text-[#D83131] transition-colors">NEUROVIBE.</a>
            <div class="hidden md:flex gap-8 text-[10px] font-bold tracking-widest uppercase items-center">
                <a href="/om-sajten.html" class="hover:text-white transition-colors">Om oss</a>
                <button onclick="window.location.href='/#access'" class="bg-white/10 px-4 py-2 rounded-full hover:bg-white/20 transition-all border border-white/10 text-white">Få tillgång</button>
            </div>

            <!-- Mobile Menu Button -->
            <button class="md:hidden text-white p-2" id="mobile-menu-btn" onclick="toggleMobileMenu()" aria-label="Meny">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M3 12h18M3 6h18M3 18h18"/></svg>
            </button>
        </div>
    </nav>
    
    <!-- Mobile Menu Overlay -->
    <div id="mobile-menu" class="fixed inset-0 bg-[#050505]/95 backdrop-blur-lg z-40 hidden flex-col items-center justify-center gap-8 text-xl font-semibold opacity-0 transition-opacity duration-300">
        <button class="absolute top-6 right-6 text-white p-2" onclick="toggleMobileMenu()" aria-label="Stäng">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        <a href="/#philosophy" class="hover:text-[#D83131] transition-colors" onclick="toggleMobileMenu()">Filosofi</a>
        <a href="/resurser.html" class="hover:text-[#D83131] transition-colors" onclick="toggleMobileMenu()">Resurser & Artiklar</a>
        <a href="/om-sajten.html" class="hover:text-[#D83131] transition-colors" onclick="toggleMobileMenu()">Om oss</a>
        <button onclick="window.location.href='/#access'; toggleMobileMenu();" class="bg-[#D83131] px-6 py-3 rounded-full hover:bg-[#B72A2A] transition-all text-sm text-white mt-4">Få tillgång</button>
    </div>
"""

content = re.sub(r'<!-- Navigation \(matches existing\) -->.*?</nav>', nav_html, content, flags=re.DOTALL)
content = re.sub(r'<main class="container mx-auto px-4 pt-24 pb-12 flex-grow max-w-4xl">', '<main class="max-w-4xl mx-auto px-4 pt-8 pb-12 flex-grow">', content)
content = re.sub(r'<article class="bg-\[#111111\] rounded-xl shadow-md p-8 md:p-12">', '<article class="glass-panel p-8 md:p-12">', content)

content = content.replace('text-dark', 'text-white')

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'w') as f:
    f.write(content)

print("Updated nav.")
