import os

files_to_update = {
    'autism-arbetsplatsen-tips-guide.html': {
        'headline': 'Autism på arbetsplatsen: Komplett guide för chefer',
        'description': 'Praktiska tips och strategier för att skapa en arbetsmiljö där autistiska medarbetare kan trivas och prestera.'
    },
    'fem-tips-for-chefer.html': {
        'headline': '5 Tips för Chefer: Så stöttar du NPF på jobbet',
        'description': 'Konkreta råd för chefer som vill skapa en mer neuroinkluderande och produktiv arbetsplats.'
    },
    'intervju-guide.html': {
        'headline': 'Neuroinkluderande Intervjuguide',
        'description': 'Bygg en neuroinkluderande intervjumall som mäter kompetens, inte förmågan att kallprata.'
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
  "@type": "Article",
  "headline": "{schema_data['headline']}",
  "description": "{schema_data['description']}",
  "url": "https://neurovibe.se/{filename}",
  "author": {{
    "@type": "Organization",
    "name": "Neurovibe"
  }},
  "publisher": {{
    "@type": "Organization",
    "name": "Neurovibe",
    "logo": {{
      "@type": "ImageObject",
      "url": "https://neurovibe.se/favicon.svg"
    }}
  }}
}}
</script>'''
        
        # Insert before </head>
        content = content.replace('</head>', schema_json + '\n</head>')
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Added schema to {filename}")

