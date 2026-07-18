import sys
from datetime import datetime
import xml.etree.ElementTree as ET

def add_to_sitemap(url):
    sitemap_path = '/data/workspace/projects/neurovibe/static/sitemap.xml'
    
    ET.register_namespace('', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    tree = ET.parse(sitemap_path)
    root = tree.getroot()
    
    # Check if URL already exists
    ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    for loc in root.findall('.//sm:loc', ns):
        if loc.text == url:
            print(f"{url} already in sitemap.")
            return

    new_url = ET.Element('url')
    loc = ET.SubElement(new_url, 'loc')
    loc.text = url
    lastmod = ET.SubElement(new_url, 'lastmod')
    lastmod.text = datetime.now().strftime('%Y-%m-%d')
    
    root.append(new_url)
    tree.write(sitemap_path, encoding='utf-8', xml_declaration=True)
    print(f"Added {url} to sitemap.xml")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        add_to_sitemap(sys.argv[1])
    else:
        print("Please provide URL")
