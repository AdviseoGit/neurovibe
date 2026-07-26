import re

def update_tack_html():
    filepath = '/data/workspace/projects/neurovibe/static/tack.html'
    
    with open(filepath, 'r') as f:
        content = f.read()

    # Update tack.html to link to the new arbetsgivarpaketet.html
    old_text = "['Läs lagkraven först',\n                         'Vad AFS 2020:5 och diskrimineringslagen faktiskt kräver av er — bra att ha läst innan vi pratar.',\n                         '/lagkrav-anpassningar-arbetsmiljo.html']"
    
    new_text = "['Ladda ner arbetsgivarpaketet',\n                         'Mallar, checklistor och rutiner enligt AFS 2020:5. Ladda ner dem här och nu.',\n                         '/arbetsgivarpaketet.html']"

    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(filepath, 'w') as f:
            f.write(content)
        print("Updated tack.html successfully.")
    else:
        print("Could not find the target text in tack.html.")

update_tack_html()
