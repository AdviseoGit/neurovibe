#!/usr/bin/env python3
"""
Internal Linking Strategy for Neurovibe
Adds contextual internal links to all 6 core articles
"""

articles = {
    "static/neurodiversitet-arbetsplatsen.html": [
        # Already has some links, add more
        ("Att skapa en neuroinkluderande miljö", 'Att skapa en <a href="fordelarna-med-neurodiversitet.html" class="text-blue-400 hover:text-blue-300 underline">neuroinkluderande miljö</a>'),
        ("problemlösningsförmågor värdesätts", 'problemlösningsförmågor <a href="npf-arbetslivet.html" class="text-blue-400 hover:text-blue-300 underline">värdesätts</a>'),
    ],
    
    "static/npf-arbetslivet.html": [
        ("arbetsplatsanpassningar", '<a href="adhd-anpassningar-jobb.html" class="text-blue-400 hover:text-blue-300 underline">arbetsplatsanpassningar</a>'),
        ("maskering på jobbet", '<a href="maskering-pa-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">maskering på jobbet</a>'),
        ("Uppgiftsnedbrytaren", '<a href="verktyg-nedbrytare.html" class="text-blue-400 hover:text-blue-300 underline">Uppgiftsnedbrytaren</a>'),
        ("neuroinkluderande arbetsplatser", '<a href="neurodiversitet-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">neuroinkluderande arbetsplatser</a>'),
    ],
    
    "static/adhd-anpassningar-jobb.html": [
        ("Fokus Timer", '<a href="verktyg-fokus-timer.html" class="text-blue-400 hover:text-blue-300 underline">Fokus Timer</a>'),
        ("Uppgiftsnedbrytaren", '<a href="verktyg-nedbrytare.html" class="text-blue-400 hover:text-blue-300 underline">Uppgiftsnedbrytaren</a>'),
        ("utbrändhet", '<a href="verktyg-burnout-kalkylator.html" class="text-blue-400 hover:text-blue-300 underline">utbrändhet</a>'),
        ("maskering", '<a href="maskering-pa-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">maskering</a>'),
    ],
    
    "static/maskering-pa-arbetsplatsen.html": [
        ("ADHD-anpassningar", '<a href="adhd-anpassningar-jobb.html" class="text-blue-400 hover:text-blue-300 underline">ADHD-anpassningar</a>'),
        ("burnout", '<a href="verktyg-burnout-kalkylator.html" class="text-blue-400 hover:text-blue-300 underline">burnout</a>'),
        ("NPF på arbetsplatsen", '<a href="npf-arbetslivet.html" class="text-blue-400 hover:text-blue-300 underline">NPF på arbetsplatsen</a>'),
        ("neuroinkluderande", '<a href="neurodiversitet-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">neuroinkluderande</a>'),
    ],
    
    "static/fordelarna-med-neurodiversitet.html": [
        ("maskering", '<a href="maskering-pa-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">maskering</a>'),
        ("arbetsplatsanpassningar", '<a href="adhd-anpassningar-jobb.html" class="text-blue-400 hover:text-blue-300 underline">arbetsplatsanpassningar</a>'),
        ("NPF i arbetslivet", '<a href="npf-arbetslivet.html" class="text-blue-400 hover:text-blue-300 underline">NPF i arbetslivet</a>'),
    ],
    
    "static/article_adhd_workplace.html": [
        ("Uppgiftsnedbrytaren", '<a href="verktyg-nedbrytare.html" class="text-blue-400 hover:text-blue-300 underline">Uppgiftsnedbrytaren</a>'),
        ("Fokus Timer", '<a href="verktyg-fokus-timer.html" class="text-blue-400 hover:text-blue-300 underline">Fokus Timer</a>'),
        ("neuroinkluderande arbetsplats", '<a href="neurodiversitet-arbetsplatsen.html" class="text-blue-400 hover:text-blue-300 underline">neuroinkluderande arbetsplats</a>'),
    ],
}

import re

for filepath, replacements in articles.items():
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        changes_made = 0
        for old_text, new_text in replacements:
            # Only replace if not already a link and exists in content
            if old_text in content and new_text not in content and f'href' not in content[max(0, content.find(old_text)-50):content.find(old_text)+50]:
                # Find first occurrence that's NOT already in a link
                pattern = f'(?<!<a[^>]*>)(?<!href=")({re.escape(old_text)})(?![^<]*</a>)'
                if re.search(pattern, content):
                    content = re.sub(pattern, new_text, content, count=1)
                    changes_made += 1
        
        if changes_made > 0:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ {filepath}: Added {changes_made} internal links")
        else:
            print(f"⏭️  {filepath}: No new links needed (already linked or text not found)")
    
    except Exception as e:
        print(f"❌ {filepath}: Error - {e}")

print("\n✅ Internal linking pass complete!")
