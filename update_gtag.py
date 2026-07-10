import re
import os

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'r') as f:
    content = f.read()

gtag_script = """<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-YJG1D5GJPR"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-YJG1D5GJPR');
</script>
"""

content = content.replace('<head>', f'<head>\n{gtag_script}')

with open('/data/workspace/projects/neurovibe/static/inkluderande-rekrytering-npf.html', 'w') as f:
    f.write(content)

print("Updated gtag.")
