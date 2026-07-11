with open('PROGRESS_LOG.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_line = "2026-07-11 | SEO | Fixade sitemap-indexering för två nya URL:er | Indexering | nästa: Bygg ut datarapport med insamlad myndighets- och burnout-data\n"
with open('PROGRESS_LOG.md', 'w', encoding='utf-8') as f:
    f.write(new_line)
    f.writelines(lines[1:])
