import xml.etree.ElementTree as ET
from datetime import datetime

tree = ET.parse('/data/workspace/projects/neurovibe/static/sitemap.xml')
root = tree.getroot()

namespace = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')

urls = [elem.find('sm:loc', namespace).text for elem in root.findall('sm:url', namespace) if elem.find('sm:loc', namespace) is not None]

new_urls = [
    'https://neurovibe.se/verktyg-anpassningsgenerator.html',
    'https://neurovibe.se/arbetsprovning-2026-forsakringskassan.html'
]

changed = False
today = datetime.now().strftime('%Y-%m-%d')

for url in new_urls:
    if url not in urls:
        new_url_elem = ET.Element('url')
        loc_elem = ET.SubElement(new_url_elem, 'loc')
        loc_elem.text = url
        lastmod_elem = ET.SubElement(new_url_elem, 'lastmod')
        lastmod_elem.text = today
        priority_elem = ET.SubElement(new_url_elem, 'priority')
        priority_elem.text = '0.8'
        root.append(new_url_elem)
        changed = True
        print(f"Added {url} to sitemap")

if changed:
    tree.write('/data/workspace/projects/neurovibe/static/sitemap.xml', encoding='UTF-8', xml_declaration=True)
    print("Sitemap updated.")
else:
    print("No changes to sitemap.")
