import re

def insert_lead_capture_ui():
    with open('/data/workspace/projects/neurovibe/static/index.html', 'r') as f:
        content = f.read()

    target = '</header>'
    
    lead_capture_html = """
    <!-- HERO LEAD CAPTURE -->
    <section class="max-w-4xl mx-auto mb-16 relative">
        <div class="absolute inset-0 bg-gradient-to-r from-blue-500/10 to-purple-500/10 rounded-2xl blur-xl border border-white/5"></div>
        <div class="relative bg-[#0F0F0F] border border-white/10 rounded-2xl p-8 md:p-12 overflow-hidden group hover:border-white/20 transition-colors">
            
            <div class="flex flex-col md:flex-row items-center gap-8 md:gap-12 relative z-10">
                <div class="flex-1 space-y-4">
                    <div class="inline-flex items-center space-x-2 px-3 py-1 bg-white/5 border border-white/10 rounded-full mb-2">
                        <div class="w-2 h-2 rounded-full bg-blue-400"></div>
                        <span class="text-xs font-semibold uppercase tracking-wider text-white">Arbetsgivarpaketet 2026</span>
                    </div>
                    <h2 class="text-2xl md:text-3xl font-bold tracking-tight">Redo att sluta gissa?</h2>
                    <p class="text-[#A0A0A0] text-sm md:text-base leading-relaxed">
                        Få våra tre mest använda mallar för neuroinkluderande ledarskap direkt till inkorgen. Skapade utifrån data, inte tyckande.
                    </p>
                    <ul class="text-sm text-[#A0A0A0] space-y-2 mt-4 mb-6">
                        <li class="flex items-center gap-2"><svg class="w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Inkluderande Möteschecklista</li>
                        <li class="flex items-center gap-2"><svg class="w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> Mjukstartsmall (Post-Semester)</li>
                        <li class="flex items-center gap-2"><svg class="w-4 h-4 text-white/40" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path></svg> ROI-Kalkylator (Kognitiv Ergonomi)</li>
                    </ul>
                </div>
                
                <div class="w-full md:w-[320px] shrink-0 bg-[#151515] p-6 rounded-xl border border-white/5">
                    <form data-nv-lead data-segment="arbetsgivare" data-source="hero_optin">
                        <input type="hidden" name="lead_magnet" value="arbetsgivarpaketet">
                        <div class="space-y-4">
                            <div>
                                <label class="block text-xs uppercase tracking-wider text-[#808080] font-semibold mb-2">Arbetsmejl</label>
                                <input type="email" name="email" required placeholder="namn@företag.se" class="w-full bg-[#0a0a0a] border border-white/10 rounded-lg px-4 py-3 text-white placeholder-[#505050] focus:outline-none focus:border-white/30 transition-colors text-sm">
                            </div>
                            <button type="submit" class="w-full bg-white text-black font-semibold rounded-lg px-4 py-3 text-sm hover:bg-gray-200 transition-colors flex items-center justify-center gap-2">
                                Skicka materialet
                                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"></path></svg>
                            </button>
                            <div class="flex items-start gap-2">
                                <input type="checkbox" name="consent" id="hero-consent" required class="mt-1 bg-transparent border-white/20 rounded-sm">
                                <label for="hero-consent" class="text-[10px] leading-tight text-[#606060] font-light cursor-pointer">
                                    Jag godkänner att Neurovibe lagrar min mejl och skickar relevanta uppdateringar. Ingen spam.
                                </label>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
            
        </div>
    </section>
    """
    
    if '<!-- HERO LEAD CAPTURE -->' not in content:
        # insert below the hero text
        hero_target = '</p>\n            </div>'
        content = content.replace(hero_target, hero_target + '\n' + lead_capture_html, 1)
        
        with open('/data/workspace/projects/neurovibe/static/index.html', 'w') as f:
            f.write(content)
        print("Added Hero Lead Capture to index.html")
    else:
        print("Hero Lead Capture already exists.")

if __name__ == "__main__":
    insert_lead_capture_ui()
