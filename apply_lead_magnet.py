import glob
import os

target_files = [
    'adhd-diagnos-vuxen.html',
    'forsakringskassan-arbetsformedlingen-stod.html',
    'maskering-pa-arbetsplatsen.html',
    'neurodiversitet-arbetsplatsen.html',
    'npf-arbetslivet.html'
]

lead_magnet_html = """
<!-- Lead Magnet -->
<div id="lead-magnet-container"></div>
<script>
fetch("/lead-magnet-snippet.html").then(r => r.text()).then(html => document.getElementById("lead-magnet-container").innerHTML = html);
</script>
"""

base_dir = '/data/workspace/projects/neurovibe/static'

for filename in target_files:
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"Not found: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    if 'lead-magnet-snippet.html' in content:
        print(f"Already applied to: {filename}")
        continue
        
    # Find </article> and insert before it
    if '</article>' in content:
        content = content.replace('</article>', lead_magnet_html + '\n</article>')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Applied to: {filename}")
    else:
        print(f"No </article> found in {filename}")

