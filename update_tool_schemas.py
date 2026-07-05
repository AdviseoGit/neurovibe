import os

files_to_update = {
    'verktyg-burnout-kalkylator.html': {
        'name': 'Burnout Prevention Calculator',
        'description': 'Mät din riskzon baserat på sensorisk belastning, maskering och kognitiva krav för att förhindra autistisk utmattning.'
    },
    'verktyg-anpassningsgenerator.html': {
        'name': 'Anpassningsgeneratorn',
        'description': 'Välj dina största utmaningar i arbetsmiljön och få ett konkret, färdigt förslag på anpassningar att ta med till chefen.'
    },
    'verktyg-fokus-timer.html': {
        'name': 'Fokus Timer',
        'description': 'En visuell timer anpassad för neurodiversitet med korta arbetspass och tydlig struktur för att hantera tidsuppfattning.'
    },
    'verktyg-nedbrytare.html': {
        'name': 'Uppgiftsnedbrytaren',
        'description': 'Övervinn exekutiv dysfunktion. Få överväldigande uppgifter nedbrutna i tre extremt små, hanterbara steg.'
    }
}

directory = '/data/workspace/projects/neurovibe/static'

for filename, schema_data in files_to_update.items():
    filepath = os.path.join(directory, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    if 'application/ld+json' not in content:
        schema_json = f'''
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{schema_data['name']}",
  "url": "https://neurovibe.se/{filename}",
  "description": "{schema_data['description']}",
  "applicationCategory": "HealthApplication",
  "operatingSystem": "All"
}}
</script>'''
        
        # Insert before </head>
        content = content.replace('</head>', schema_json + '\n</head>')
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Added schema to {filename}")

