"""Pre-deploy gate for the redesigned site. Crawls every page from the sitemap on a running server and fails on:
  - any internal link that does not answer 200 (or a deliberate 301)
  - a page without <title>, meta description (unless noindex) or exactly one <h1>
  - a canonical that does not point at the page itself
  - leftovers from the old site: Tailwind classes, AFS 2020:5 outside history notes, fetch of /nav.html
    python3 tools_build/check_site.py [base]"""
import re, sys, json, urllib.request, urllib.error
from html.parser import HTMLParser

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8099').rstrip('/')
SITE = 'https://neurovibe.se'


def get(path):
    req = urllib.request.Request(BASE + path, headers={'User-Agent': 'nv-check'})
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, *a, **k): return None
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(req) as r: return r.status, r.read().decode('utf-8', 'replace')
    except urllib.error.HTTPError as e: return e.code, ''


class P(HTMLParser):
    def __init__(self):
        super().__init__(); self.links = set(); self.h1 = 0; self.title = ''; self._t = False; self.desc = None; self.canon = None; self.robots = ''
    def handle_starttag(self, tag, a):
        a = dict(a)
        if tag == 'a' and a.get('href'): self.links.add(a['href'])
        if tag == 'h1': self.h1 += 1
        if tag == 'title': self._t = True
        if tag == 'meta' and a.get('name') == 'description': self.desc = a.get('content')
        if tag == 'meta' and a.get('name') == 'robots': self.robots = a.get('content', '')
        if tag == 'link' and a.get('rel') == 'canonical': self.canon = a.get('href')
    def handle_endtag(self, tag):
        if tag == 'title': self._t = False
    def handle_data(self, d):
        if self._t: self.title += d


code, sm = get('/sitemap.xml')
paths = [re.sub(r'^https?://[^/]+', '', u) or '/' for u in re.findall(r'<loc>([^<]+)</loc>', sm)]
paths += ['/tack.html', '/feedback.html']
problems, link_targets = [], set()
for path in paths:
    code, html = get(path)
    if code != 200: problems.append(f'{path}: {code}'); continue
    p = P(); p.feed(html)
    noindex = 'noindex' in p.robots
    if not p.title.strip(): problems.append(f'{path}: tom title')
    if not noindex and not p.desc: problems.append(f'{path}: saknar meta description')
    if p.h1 != 1: problems.append(f'{path}: {p.h1} h1')
    if p.canon != SITE + path: problems.append(f'{path}: canonical {p.canon}')
    if re.search(r'class="[^"]*\b(text-\[|bg-\[|md:|glass-panel|prose-invert)', html): problems.append(f'{path}: Tailwind-rester')
    if '/nav.html' in html: problems.append(f'{path}: hämtar /nav.html')
    for m in re.finditer(r'AFS 2020:5', html):
        ctx = html[max(0, m.start() - 80):m.end() + 40]
        if 'ersatte' not in ctx and 'upphävd' not in ctx and 'rutinmall-afs-2020-5' not in ctx:
            problems.append(f'{path}: nämner AFS 2020:5 som gällande'); break
    for ld in re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S):
        try: json.loads(ld)
        except Exception as e: problems.append(f'{path}: ogiltig JSON-LD ({e})')
    for href in p.links:
        h = href.split('#')[0].split('?')[0]
        if h.startswith(SITE): h = h[len(SITE):] or '/'
        if h.startswith('/') and not h.startswith('//'): link_targets.add((h, path))
seen = {}
for target, src in sorted(link_targets):
    if target not in seen: seen[target] = get(target)[0]
    if seen[target] not in (200, 301): problems.append(f'trasig länk {target} ({seen[target]}) på {src}')
print(f'{len(paths)} sidor, {len(seen)} interna mål kontrollerade')
if problems:
    print('\n'.join(sorted(set(problems)))); sys.exit(1)
print('GRINDEN GRÖN')
