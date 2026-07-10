import re
import os

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'r') as f:
    content = f.read()

# Replace tailwind config and basic styling
content = re.sub(r'<html lang="sv" class="[^"]*">', '<html lang="sv" class="bg-[#050505]">', content)
content = re.sub(r'<script>\s*tailwind.config.*?</script>', '', content, flags=re.DOTALL)
content = re.sub(r'<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">', '<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap" rel="stylesheet">', content)

# update colors class
content = content.replace('bg-light', 'bg-[#050505]')
content = content.replace('bg-dark', 'bg-[#0A0A0A]')
content = content.replace('bg-white', 'bg-[#111111]')
content = content.replace('text-gray-900', 'text-white')
content = content.replace('text-gray-800', 'text-white')
content = content.replace('text-gray-700', 'text-[#D0D0D0]')
content = content.replace('text-gray-600', 'text-[#A0A0A0]')
content = content.replace('text-gray-400', 'text-[#A0A0A0]')
content = content.replace('text-primary', 'text-[#D83131]')
content = content.replace('bg-primary', 'bg-[#D83131]')
content = content.replace('hover:bg-primary-dark', 'hover:bg-[#B72A2A]')
content = content.replace('text-secondary', 'text-[#D83131]')
content = content.replace('border-gray-200', 'border-white/10')
content = content.replace('border-gray-700', 'border-white/10')

# update typography
content = content.replace('font-sans', 'font-inter')

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'w') as f:
    f.write(content)

print("Updated theme.")
