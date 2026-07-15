with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()
    
new_log = "2026-07-15 | INNEHÅLL/SEO | Utökat ADHD-Diagnos guiden till >3000 ord och implementerat FAQ + Article Schema | Innehållsbyggande & SEO | nästa: Expandera Försäkringskassan-guiden\n"
content = new_log + content

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(content)
