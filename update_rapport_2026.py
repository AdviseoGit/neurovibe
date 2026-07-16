import re

with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_section = """
                <h2 class="text-2xl font-bold mb-4 text-white">Insikt 3: Stödet når inte fram (Myndighetsdata)</h2>
                <p class="mb-8 text-[#A0A0A0]">
                    Datumet från Myndighetsnavigatorn belyser ett kritiskt glapp mellan tillgängligt stöd och utnyttjandegrad. Majoriteten av användarna söker stöd för kognitiv överbelastning, men få är medvetna om möjligheten till kognitiva hjälpmedel via Försäkringskassan. Det är en hög tröskel för neurodivergenta individer att driva dessa processer på egen hand, vilket understryker vikten av proaktivt arbetsgivaransvar.
                </p>
                <div class="glass-panel p-8 border-[#D83131]/30 mb-12">
"""

content = content.replace('                <div class="glass-panel p-8 border-[#D83131]/30 mb-12">', new_section)
content = content.replace('(Burnout Calculator och Uppgiftsnedbrytaren)', '(Burnout Calculator, Uppgiftsnedbrytaren och Myndighetsnavigatorn)')
content = content.replace('under maj-juni 2026.', 'under Q2 2026.')

with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'w', encoding='utf-8') as f:
    f.write(content)
