with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'r') as f:
    content = f.read()
    
new_log = "2026-07-15 | INNEHÅLL/SEO | Expanderade Försäkringskassan-guiden med nya lönebidragsregler och konverterade till HTML med Schema.org | Innehållsbyggande & SEO | nästa: Bygg ut datarapport med insamlad myndighets- och burnout-data\n"
content = new_log + content

with open('/data/workspace/projects/neurovibe/PROGRESS_LOG.md', 'w') as f:
    f.write(content)
