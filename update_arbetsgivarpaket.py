import os
import re

file_path = "/data/workspace/projects/neurovibe/static/arbetsgivarpaketet.html"
with open(file_path, "r") as f:
    content = f.read()

# Ersätt Dokument 4 med en riktig Samtalsmall
new_doc_4 = """
            <div class="glass-panel p-8 rounded-2xl mt-6">
                <div class="flex flex-col md:flex-row md:items-start justify-between gap-6">
                    <div>
                        <div class="text-[#D83131] font-mono text-xs tracking-widest uppercase mb-2">Dokument 4 av 5</div>
                        <h2 class="text-2xl font-bold mb-3">Samtalsmall (Chef/Medarbetare)</h2>
                        <p class="text-[#A0A0A0] mb-6">10 frågor för chefen att ställa för att kartlägga behov utan att prata medicin/diagnos. Fokus ligger på arbetsmiljö och hinder.</p>
                    </div>
                </div>
                <div class="bg-black/50 border border-white/5 rounded-xl p-6 text-sm text-[#E0E0E0] leading-relaxed">
                    <p class="mb-4"><strong>Att tänka på inför samtalet:</strong> Fråga aldrig efter en diagnos. Använd öppna frågor och fokusera på lösningar snarare än problem. Målet är att identifiera var friktionen uppstår.</p>
                    <ul class="list-decimal pl-5 mb-4 text-[#A0A0A0] space-y-3">
                        <li>Vilka arbetsuppgifter eller situationer dränerar dig mest på energi under en vanlig vecka?</li>
                        <li>När upplever du att du har lättast att fokusera och få saker gjorda? Kan vi återskapa de förutsättningarna oftare?</li>
                        <li>Hur upplever du ljudnivån och den visuella miljön runt din arbetsplats?</li>
                        <li>Hur vill du helst ta emot instruktioner för nya uppgifter (muntligt, skriftligt, steg-för-steg)?</li>
                        <li>Upplever du att det är tydligt vad som förväntas av dig och när en uppgift är "klar"?</li>
                        <li>Hur fungerar våra möten för dig? Behöver vi ändra på agendor, längd eller uppföljning?</li>
                        <li>Blir du ofta avbruten under arbetsdagen? Hur skulle vi kunna minimera de avbrotten?</li>
                        <li>Har du tillräckligt med tid för återhämtning under dagen?</li>
                        <li>Finns det några specifika verktyg (mjukvara/hårdvara) som skulle underlätta ditt arbete?</li>
                        <li>Om vi bara skulle göra <strong>en</strong> förändring i din arbetsmiljö imorgon, vad skulle ha störst positiv effekt?</li>
                    </ul>
                </div>
            </div>
"""

# Hitta Dokument 4 i listan och byt ut mot en uppmaning att läsa ovan
content = re.sub(
    r'<div class="text-\[#D83131\] font-mono text-\[10px\] tracking-widest uppercase mb-2">Dokument 4</div>.*?<button onclick="alert.*?Öppna verktyg →</button>\s*</div>',
    r'<div class="text-[#D83131] font-mono text-[10px] tracking-widest uppercase mb-2">Dokument 4</div>\n                    <h3 class="font-bold mb-2">Samtalsmall (Chef/Medarbetare)</h3>\n                    <p class="text-[#A0A0A0] text-sm mb-4 flex-grow">10 frågor för chefen att ställa för att kartlägga behov utan att prata medicin/diagnos.</p>\n                    <a href="#dokument-4" onclick="document.getElementById(\'doc4\').scrollIntoView({behavior: \'smooth\'})" class="text-sm font-medium text-[#D83131] hover:underline mt-auto">Läs mallen ovan ↑</a>\n                </div>',
    content,
    flags=re.DOTALL
)

# Lägg till Dokument 4 div:en efter Dokument 2
content = content.replace("<!-- Dokument 3, 4, 5 listade -->", f"<div id=\"doc4\">{new_doc_4}</div>\n            <!-- Dokument 3, 4, 5 listade -->")

with open(file_path, "w") as f:
    f.write(content)
print("Updated arbetsgivarpaketet.html")
