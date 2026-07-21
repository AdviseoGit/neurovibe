import re

with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'r', encoding='utf-8') as f:
    content = f.read()

new_section = """
                <h2 class="text-2xl font-bold mb-4 text-white">Insikt 4: ROI för Kognitiva Proteser & Anpassningar</h2>
                <p class="mb-8 text-[#A0A0A0]">
                    Tidig data från vår AI ROI-kalkylator (Q3 2026) pekar på en massiv outnyttjad potential. Genom att implementera rätt anpassningar – såsom att minska sensorisk belastning (masking) och tillhandahålla kognitiva AI-verktyg – uppskattas företag kunna spara i snitt 150 000 till 300 000 SEK per individ och år genom minskad personalomsättning och ökad produktivitet, framförallt hos de som identifierar sig med ADHD och Autism.
                </p>
                <div class="glass-panel p-8 border-[#D83131]/30 mb-12">
"""

if "Insikt 4: ROI för Kognitiva Proteser" not in content:
    content = content.replace('                <div class="glass-panel p-8 border-[#D83131]/30 mb-12">', new_section)
    with open('/data/workspace/projects/neurovibe/static/data-rapport-2026.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Added Insight 4")
else:
    print("Insight 4 already exists")
