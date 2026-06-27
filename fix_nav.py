import os
import re

html_files = [f for f in os.listdir("/data/workspace/projects/neurovibe/static") if f.endswith(".html")]

nav_replacement = """
    <!-- Navbar -->
    <nav class="fixed w-full z-50 bg-[#050505]/80 backdrop-blur-md border-b border-white/5">
        <div class="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
            <a href="/" class="flex items-center gap-2 group">
                <div class="w-8 h-8 rounded bg-gradient-to-br from-[#D83131] to-[#FF5555] flex items-center justify-center font-bold text-white shadow-lg shadow-[#D83131]/20 group-hover:shadow-[#D83131]/40 transition-all">N</div>
                <span class="text-xl font-bold tracking-tight text-white">Neurovibe</span>
            </a>

            <!-- Desktop Menu -->
            <div class="hidden md:flex gap-8 text-[10px] font-bold tracking-widest uppercase items-center text-white/60">
                <a href="/#philosophy" class="hover:text-white transition-colors">Filosofi</a>
                <a href="/#lab" class="hover:text-white transition-colors">Labbet</a>
                <a href="/resurser.html" class="text-[#D83131] hover:text-[#FF5555] transition-colors">Resurser & Artiklar</a>
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

mobile_menu_script = """
    <script>
        function toggleMobileMenu() {
            const menu = document.getElementById('mobile-menu');
            if (menu.classList.contains('hidden')) {
                menu.classList.remove('hidden');
                setTimeout(() => menu.classList.remove('opacity-0'), 10);
                document.body.style.overflow = 'hidden'; // Prevent scrolling
            } else {
                menu.classList.add('opacity-0');
                setTimeout(() => {
                    menu.classList.add('hidden');
                    document.body.style.overflow = '';
                }, 300);
            }
        }
    </script>
"""

# Apply to a few tools
tools = ["verktyg-burnout-kalkylator.html", "verktyg-fokus-timer.html", "intervju-guide.html"]
for t in tools:
    p = os.path.join("/data/workspace/projects/neurovibe/static", t)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            c = f.read()
        
        # Replace existing nav
        c = re.sub(r'<!-- Navbar -->.*?</div>\s*</div>\s*(?:</nav>|<!-- Mobile Menu Overlay -->.*?</div>)', nav_replacement, c, flags=re.DOTALL)
        # Handle case where nav ends earlier
        c = re.sub(r'<nav class="fixed.*?<!-- Mobile Menu Overlay -->.*?</div>', nav_replacement, c, flags=re.DOTALL)
        
        if "function toggleMobileMenu()" not in c:
            c = c.replace("</body>", mobile_menu_script + "\n</body>")
            
        with open(p, "w", encoding="utf-8") as f:
            f.write(c)
        print(f"Updated nav in {t}")
