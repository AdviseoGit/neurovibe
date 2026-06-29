import re

with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'r') as f:
    content = f.read()

# Add AI disclaimer paragraph
ai_disclaimer = """<div class="glass-panel p-6 border-l-4 border-[#D83131] mb-12">
                        <h2 style="margin-top: 0;">Ett AI-drivet experiment</h2>
                        <p class="text-[#A0A0A0]">Denna sajt skapas och drivs helt av autonoma AI-agenter. Vi använder AI för att sammanställa, strukturera och bygga verktyg kring neurodiversitet. Det finns inga mänskliga ämnesexperter, läkare eller psykologer bakom innehållet. Innehållet är välresearchat men kan innehålla fel och utgör <strong class="text-white">aldrig medicinsk rådgivning eller professionellt stöd</strong>. Fatta viktiga beslut i samråd med en kvalificerad expert.</p>
                    </div>"""
    
content = content.replace(
    '<h2>Vårt Uppdrag</h2>',
    ai_disclaimer + '\n\n                        <h2>Vårt Uppdrag</h2>'
)

# Neutralize "grundades ur övertygelsen" and "Vilka vi är" if they exist
content = content.replace(
    'Neurovibe grundades ur övertygelsen att neurodiversitet är en strategisk tillgång.',
    'Neurovibe bygger på övertygelsen att neurodiversitet är en strategisk tillgång.'
)

content = content.replace(
    '<h2>Vilka vi är</h2>',
    '<h2>Vilka vi är (och inte är)</h2>'
)

content = content.replace(
    '<p>\n                            Vi är ett dedikerat team som brinner för att brygga gapet mellan neurodivergenta talanger och moderna arbetsplatser. Vi kombinerar insikter från arbetspsykologi med praktisk erfarenhet av kognitiva anpassningar för att skapa resurser som gör verklig skillnad.\n                        </p>',
    '<p>\n                            Sajten och dess verktyg underhålls och genereras helt av AI-agenter inom fastställda mänskliga ramverk (guardrails). Vårt fokus är att strukturera information och bygga dopaminvänliga verktyg som gör vardagen lite enklare, men vi är inga mänskliga experter eller psykologer.\n                        </p>'
)

with open('/data/workspace/projects/neurovibe/static/om-sajten.html', 'w') as f:
    f.write(content)
