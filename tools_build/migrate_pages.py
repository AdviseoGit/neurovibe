"""One-off migration: old static/*.html content pages -> content_pages/<slug>.html + site/pages.json.

Keeps every URL, title, meta description and JSON-LD. Strips the old Tailwind markup,
inline lead forms and scripts so the content renders in the shared "Lugn struktur" layout.
Re-runnable: it only reads static/ and overwrites its own outputs.

    python3 tools_build/migrate_pages.py
"""
import json, re
from pathlib import Path
from bs4 import BeautifulSoup, Tag, NavigableString, Comment

ROOT = Path(__file__).resolve().parent.parent
STATIC = ROOT / 'static'
OUT = ROOT / 'content_pages'
# content_pages/ is the source of truth after the migration and has been edited by hand
# (fact corrections). Re-running would silently undo that.
import sys
if (OUT / 'npf-arbetslivet.html').exists() and '--force' not in sys.argv:
    sys.exit('content_pages/ already migrated and edited by hand — refusing to overwrite (use --force only on purpose)')
OUT.mkdir(exist_ok=True)

# Pages that move into the article layout. Tools, the home page, admin and snippets are rebuilt by hand.
PAGES = {
    'adhd-anpassningar-jobb': 'guide', 'adhd-diagnos-guide': 'guide', 'adhd-diagnos-vuxen': 'guide',
    'ai-verktyg-neurodiversitet': 'guide', 'arbetsplats-schema-npf': 'guide',
    'arbetsprovning-2026-forsakringskassan': 'stod', 'autism-arbetsplatsen-tips-guide': 'guide',
    'data-rapport-2026': 'data', 'fem-tips-for-chefer': 'arbetsgivare', 'for-arbetsgivare': 'arbetsgivare',
    'for-medarbetare': 'medarbetare', 'fordelarna-med-neurodiversitet': 'guide',
    'forsakringskassan-arbetsformedlingen-stod': 'stod', 'inkluderande-kultur-npf': 'arbetsgivare',
    'inkluderande-rekrytering-npf': 'arbetsgivare', 'integritetspolicy': 'om',
    'kognitiv-ergonomi-npf': 'guide', 'lagkrav-anpassningar-arbetsmiljo': 'arbetsgivare',
    'maskering-pa-arbetsplatsen': 'guide', 'neurodiversitet-arbetsplatsen': 'guide', 'npf-arbetslivet': 'guide',
    'om-sajten': 'om', 'partner': 'om', 'post-semester-stress-npf': 'guide', 'redaktionell-policy': 'om',
    'arbetsgivarpaketet/anpassningsbibliotek': 'mall', 'arbetsgivarpaketet/lagkrav-oversikt': 'mall',
    'arbetsgivarpaketet/rutinmall-afs-2020-5': 'mall', 'arbetsgivarpaketet/samtalsmall-kartlaggning': 'mall',
    'arbetsgivarpaketet/stod-och-bidrag': 'mall',
}
# Which flagship tool each section points to at the end of an article.
TOOL_FOR = {'stod': 'stodkollen', 'arbetsgivare': 'anpassningsplanen', 'guide': 'anpassningsplanen',
            'medarbetare': 'anpassningsplanen', 'mall': 'anpassningsplanen', 'data': 'anpassningsplanen', 'om': None}
TOOL_OVERRIDE = {'arbetsprovning-2026-forsakringskassan': 'atergangsplanen', 'post-semester-stress-npf': 'atergangsplanen',
                 'arbetsplats-schema-npf': 'schema-generatorn', 'kognitiv-ergonomi-npf': 'fokustimern'}

KEEP_ATTRS = {'a': {'href', 'title'}, 'img': {'src', 'alt', 'width', 'height'}, 'td': {'colspan', 'rowspan'},
              'th': {'colspan', 'rowspan', 'scope'}, 'ol': {'start'}, 'time': {'datetime'}}
DROP_TAGS = {'script', 'style', 'noscript', 'form', 'nav', 'footer', 'svg', 'button', 'input', 'select',
             'textarea', 'label', 'iframe', 'canvas'}
INLINE_OK = {'a', 'strong', 'b', 'em', 'i', 'code', 'br', 'sup', 'sub', 'abbr', 'time', 'mark', 'small'}
BLOCK_OK = {'h2', 'h3', 'h4', 'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tr', 'th', 'td', 'blockquote',
            'figure', 'figcaption', 'img', 'hr', 'details', 'summary', 'dl', 'dt', 'dd', 'aside', 'section', 'caption'}

# Regulatory fix: AFS 2020:5 was repealed 2025-01-01 and replaced by AFS 2023:2, chapter 3.
REG_FIXES = [
    (re.compile(r'AFS\s*2020:5'), 'AFS 2023:2 kap. 3'),
    (re.compile(r'Arbetsanpassning\s*\(AFS 2023:2 kap\. 3\)'), 'Arbetsanpassning (AFS 2023:2 kap. 3)'),
]


def slug_of(path):
    return path[:-5] if path.endswith('.html') else path


def text_of(el):
    return re.sub(r'\s+', ' ', el.get_text(' ', strip=True)) if el else ''


def is_form_box(el):
    """A small div whose job is to sell a newsletter/PDF — it has a form or an email input and little else.
    A big content wrapper that merely CONTAINS a form somewhere must survive (only the form goes)."""
    if not isinstance(el, Tag):
        return False
    has_form = el.find('form') is not None or el.find('input', attrs={'type': 'email'}) is not None
    return has_form and len(text_of(el).split()) < 150 and not el.find(['h2', 'table'])


def tool_links(el):
    return [a for a in el.find_all('a', href=True) if re.search(r'/verktyg-|kalkylator|navigator|generator', a['href'])]


def classify_box(div):
    """Turn a styled div into a semantic block (or None to unwrap)."""
    if is_form_box(div):
        return 'drop'
    heading = div.find(['h2', 'h3', 'h4'], recursive=True)
    htxt = text_of(heading).lower() if heading else ''
    table = div.find('table')
    if table:
        # only a box that is mostly the table — a content wrapper that merely contains one is unwrapped
        return 'table' if len(text_of(table).split()) >= 0.6 * len(text_of(div).split()) else None
    if 'källor' in htxt or 'referenser' in htxt:
        return 'sources'
    links = tool_links(div)
    words = len(text_of(div).split())
    if links and words < 90:
        return 'cta'
    if heading and words < 160 and len(div.find_all(['p', 'ul', 'ol'])) <= 4 and div.find_parent('table') is None:
        return 'note'
    return None


def clean(node):
    for c in list(node.descendants):
        if isinstance(c, Comment):
            c.extract()
    for t in node.find_all(id=re.compile('lead-magnet|cookie', re.I)):
        t.decompose()
    # newsletter/PDF boxes must be recognised while their form is still there
    for div in list(node.find_all('div')):
        if div.parent is not None and is_form_box(div):
            div.decompose()
    for t in node.find_all(DROP_TAGS):
        t.decompose()
    for a in node.find_all('a'):
        if re.match(r'^\s*(←|&larr;)?\s*Tillbaka', text_of(a)):
            a.decompose()
    # classify boxes outermost-first
    for div in list(node.find_all('div')):
        if div.parent is None:
            continue
        kind = classify_box(div)
        if kind == 'drop':
            div.decompose()
        elif kind == 'table':
            cap = div.find(['h2', 'h3', 'h4'])
            table = div.find('table')
            fig = BeautifulSoup('<figure class="table-wrap"></figure>', 'html.parser').figure
            if cap and cap.find_parent('table') is None:
                c = BeautifulSoup('<figcaption></figcaption>', 'html.parser').figcaption
                c.string = text_of(cap)
                fig.append(c)
            fig.append(table.extract())
            div.replace_with(fig)
        elif kind in ('sources', 'cta', 'note'):
            div.name = 'section' if kind == 'sources' else 'aside'
            div.attrs = {'class': {'sources': 'sources', 'cta': 'callout', 'note': 'note'}[kind]}
    # unwrap generic wrappers
    for t in node.find_all(['div', 'span', 'article', 'header', 'main', 'center', 'font']):
        if t.name == 'span' and t.get('class') and any('font-bold' in c or 'font-semibold' in c for c in t.get('class')):
            t.name = 'strong'
            t.attrs = {}
            continue
        t.unwrap()
    # attributes
    for t in node.find_all(True):
        if t.name in ('aside', 'section', 'figure') and t.get('class') in (['sources'], ['callout'], ['note'], ['table-wrap']):
            t.attrs = {'class': t['class']}
            continue
        keep = KEEP_ATTRS.get(t.name, set())
        t.attrs = {k: v for k, v in t.attrs.items() if k in keep}
        if t.name == 'h1':
            t.name = 'h2'
    # empties
    changed = True
    while changed:
        changed = False
        for t in node.find_all(['p', 'li', 'ul', 'ol', 'h2', 'h3', 'h4', 'aside', 'section', 'strong', 'em', 'blockquote']):
            if not text_of(t) and not t.find('img'):
                t.decompose(); changed = True
    return node


def fix_regs(html):
    for rx, rep in REG_FIXES:
        html = rx.sub(rep, html)
    return html


def internal_links(html):
    return sorted(set(re.findall(r'href="(/[^"#?]*)', html)))


pages_meta = []
for path, section in PAGES.items():
    src = STATIC / f'{path}.html'
    soup = BeautifulSoup(src.read_text(encoding='utf-8'), 'html.parser')
    title = text_of(soup.title)
    md = soup.find('meta', attrs={'name': 'description'})
    desc = md['content'].strip() if md and md.get('content') else ''
    ld = [s.string.strip() for s in soup.find_all('script', type='application/ld+json') if s.string]
    main = soup.find('main') or soup.body
    h1 = main.find('h1') or soup.find('h1')
    h1_text = text_of(h1)
    # lead = first <p> right after the h1 (within its header block)
    lead = ''
    if h1:
        nxt = h1.find_next(['p', 'h2'])
        if nxt and nxt.name == 'p' and len(text_of(nxt).split()) > 8:
            lead = text_of(nxt); nxt.decompose()
    updated = ''
    m = re.search(r'(Uppdaterad|Senast uppdaterad|Publicerad)[:\s]+(\d{4}-\d{2}-\d{2})', text_of(main))
    if m:
        updated = m.group(2)
    # remove kicker/eyebrow and date lines above h1
    if h1:
        for sib in list(h1.find_all_previous(limit=6)):
            if isinstance(sib, Tag) and sib.name in ('span', 'p', 'div') and len(text_of(sib).split()) <= 6 and sib in main.descendants and not sib.find('h1'):
                sib.decompose()
        h1.decompose()
    for t in main.find_all(string=re.compile(r'^\s*(Uppdaterad|Senast uppdaterad)[:\s]+\d{4}-\d{2}-\d{2}\s*$')):
        par = t.parent
        if par and len(text_of(par).split()) <= 6:
            par.decompose()
    body = clean(main)
    html = fix_regs(body.decode_contents())
    html = re.sub(r'\n\s*\n+', '\n', html).strip()
    slug = slug_of(path)
    out = OUT / f'{slug}.html'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(html + '\n', encoding='utf-8')
    tool = TOOL_OVERRIDE.get(slug, TOOL_FOR[section])
    pages_meta.append({
        'path': f'{path}.html', 'slug': slug, 'section': section,
        'title': fix_regs(title), 'description': fix_regs(desc), 'h1': fix_regs(h1_text), 'lead': fix_regs(lead),
        'updated': updated, 'jsonld': [fix_regs(x) for x in ld], 'tool': tool,
        'noindex': path in ('tack', 'feedback'), 'words': len(BeautifulSoup(html, 'html.parser').get_text(' ').split()),
        'links': internal_links(html),
    })
    print(f"{path:48} {section:12} h1={h1_text[:40]!r:44} lead={bool(lead)!s:5} upd={updated or '-':10} words={pages_meta[-1]['words']}")

(ROOT / 'site').mkdir(exist_ok=True)
(ROOT / 'site' / 'pages.json').write_text(json.dumps(pages_meta, ensure_ascii=False, indent=1), encoding='utf-8')
print('pages:', len(pages_meta))
