import os
import re

file_path = "/data/workspace/projects/neurovibe/static/for-arbetsgivare.html"
with open(file_path, "r") as f:
    content = f.read()

# Lägg till länk till arbetsgivarpaketet i texten om det
content = re.sub(
    r'<h3 class="text-xl font-bold mb-4">Arbetsgivarpaketet</h3>\s*<p class="text-\[#A0A0A0\] text-\[15px\] leading-relaxed mb-6 flex-grow">\s*Mallar, anpassningsbibliotek, lagkravsöversikt och verktyg. Ni gör jobbet\s*själva, men slipper börja från ett tomt dokument.\s*</p>',
    r'<h3 class="text-xl font-bold mb-4">Arbetsgivarpaketet</h3>\n                    <p class="text-[#A0A0A0] text-[15px] leading-relaxed mb-6 flex-grow">\n                        Mallar, anpassningsbibliotek, lagkravsöversikt och verktyg. Ni gör jobbet\n                        själva, men slipper börja från ett tomt dokument. Ladda ner de 5 dokumenten direkt.\n                    </p>',
    content
)

with open(file_path, "w") as f:
    f.write(content)
print("Updated for-arbetsgivare.html")
