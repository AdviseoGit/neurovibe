"""List the elements wider than the viewport at phone width. python3 tools_build/find_overflow.py /path ..."""
import sys
from playwright.sync_api import sync_playwright
BASE = 'http://localhost:8099'
JS = """() => { const w = document.documentElement.clientWidth, out = [];
  for (const el of document.querySelectorAll('body *')) { const r = el.getBoundingClientRect();
    if (r.right > w + 1 && r.width > 0) out.push(el.tagName.toLowerCase() + (el.id ? '#' + el.id : '') + (el.className && typeof el.className === 'string' ? '.' + el.className.split(' ')[0] : '') + ' right=' + Math.round(r.right) + ' w=' + Math.round(r.width) + ' "' + (el.textContent || '').trim().slice(0, 40) + '"'); }
  return out.slice(0, 12); }"""
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for path in sys.argv[1:] or ['/']:
        p = b.new_page(viewport={'width': 390, 'height': 800}); p.goto(BASE + path)
        print(path); [print('  ', x) for x in p.evaluate(JS)]
    b.close()
