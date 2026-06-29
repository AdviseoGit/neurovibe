import re

with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'r') as f:
    content = f.read()

# Make sure AI transparency is clear and no human expert is implied.
if "Vårt uppdrag" in content and "Drivs av AI" not in content:
    # Add AI disclaimer paragraph
    ai_disclaimer = """<div class="glass-panel p-6 border-l-4 border-[#D83131] mb-8">
                    <h2 class="text-xl font-semibold text-white mb-2">Ett AI-drivet experiment</h2>
                    <p class="text-[#A0A0A0] text-sm">Denna sajt skapas och drivs helt av autonoma AI-agenter. Vi använder AI för att sammanställa, strukturera och bygga verktyg kring neurodiversitet. Det finns inga mänskliga ämnesexperter, läkare eller psykologer bakom innehållet. Innehållet är välresearchat men kan innehålla fel och utgör <strong class="text-white">aldrig medicinsk rådgivning eller professionellt stöd</strong>. Fatta viktiga beslut i samråd med en kvalificerad expert.</p>
                </div>"""
    
    content = content.replace(
        '<h2 class="text-2xl font-semibold text-white mb-4 mt-8">Vårt uppdrag</h2>',
        ai_disclaimer + '\n                <h2 class="text-2xl font-semibold text-white mb-4 mt-8">Vårt uppdrag</h2>'
    )
    
    with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'w') as f:
        f.write(content)
