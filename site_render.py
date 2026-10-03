"""Renders every HTML page of neurovibe.se from one layout ("Lugn struktur").

Content pages live as body fragments in content_pages/<slug>.html with their metadata in
site/pages.json; tools are Jinja templates in templates/tools/; hubs in templates/hubs/.
Every URL the old static site had is kept — main.py asks resolve() for a path and gets HTML or None.
"""
import json, math, os, re
from datetime import date
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent
SITE = 'https://neurovibe.se'
ASSET_V = os.environ.get('RAILWAY_GIT_COMMIT_SHA', 'dev')[:8]

env = Environment(loader=FileSystemLoader(str(ROOT / 'templates')), autoescape=select_autoescape(['html']))

PAGES = {p['path']: p for p in json.loads((ROOT / 'site/pages.json').read_text(encoding='utf-8'))}
TOOLS = json.loads((ROOT / 'site/tools.json').read_text(encoding='utf-8'))
TOOL_BY_KEY = {t['key']: t for t in TOOLS}
TOOL_BY_PATH = {t['path']: t for t in TOOLS}

SECTIONS = {
    'guide': ('Guider', '/resurser.html'), 'medarbetare': ('Guider', '/resurser.html'), 'data': ('Guider', '/resurser.html'),
    'stod': ('Stöd och regler', '/forsakringskassan-arbetsformedlingen-stod.html'),
    'arbetsgivare': ('För arbetsgivare', '/for-arbetsgivare.html'), 'mall': ('Mallar', '/arbetsgivarpaketet.html'),
    'om': ('Om Neurovibe', '/om-sajten.html'),
}
NAV = [('Verktyg', '/verktyg.html'), ('Mallar', '/arbetsgivarpaketet.html'),
       ('Stöd och regler', '/forsakringskassan-arbetsformedlingen-stod.html'), ('Guider', '/resurser.html'),
       ('För arbetsgivare', '/for-arbetsgivare.html')]

# hub / simple pages rendered from their own template: path -> (template, meta)
HUBS = {
    '': ('hubs/home.html', {'title': 'Neurovibe — verktyg och mallar för NPF i arbetslivet',
        'description': 'Svenska verktyg för ADHD, autism och NPF i arbetslivet: anpassningsplan, stödkoll för Arbetsförmedlingen och Försäkringskassan, återgångsplan och mallar för chef och HR.'}),
    'verktyg.html': ('hubs/tools.html', {'title': 'Alla verktyg för NPF i arbetslivet | Neurovibe',
        'description': 'Gratis svenska verktyg för dig med ADHD eller autism och för chef och HR: anpassningsplan, stödkoll, återgångsplan, fokustimer och mer.'}),
    'resurser.html': ('hubs/guides.html', {'title': 'Guider om NPF, ADHD och autism i arbetslivet | Neurovibe',
        'description': 'Alla Neurovibes guider om NPF i arbetslivet: anpassningar, stöd från myndigheter, lagkrav, maskering, ergonomi och ledarskap.'}),
    'arbetsgivarpaketet.html': ('hubs/templates.html', {'title': 'Mallar för arbetsanpassning vid NPF | Neurovibe',
        'description': 'Gratis mallar för chef och HR: rutin för arbetsanpassning enligt AFS 2023:2, samtalsmall, anpassningsbibliotek, lagkravsöversikt och stöd och bidrag.'}),
    'tack.html': ('hubs/simple.html', {'title': 'Tack — vi hör av oss | Neurovibe', 'noindex': True, 'kind': 'tack'}),
    'waitlist-success.html': ('hubs/simple.html', {'title': 'Du är registrerad | Neurovibe', 'noindex': True, 'kind': 'tack'}),
    'feedback.html': ('hubs/simple.html', {'title': 'Tyck till om verktygen | Neurovibe', 'noindex': True, 'kind': 'feedback'}),
}


def short(p):
    t = p['h1'] or p['title']
    t = re.split(r'\s*[:–—|]\s*', t)[0]
    return t if len(t) <= 60 else t[:57] + '…'


for p in PAGES.values():
    p['short'] = short(p)
    p['read_min'] = max(1, math.ceil(p['words'] / 200)) if p['section'] not in ('om', 'mall') else None


def nav_for(path):
    return [{'label': l, 'href': h, 'active': ('/' + path) == h} for l, h in NAV]


def canonical(path):
    return f'{SITE}/{path}' if path else f'{SITE}/'


SOCIAL = {p.stem for p in (ROOT / 'static/social').glob('*.jpg')} if (ROOT / 'static/social').exists() else set()


def og_image(page):
    slug = (page.get('slug') or '').split('/')[-1]
    return f'{SITE}/static/social/{slug}.jpg' if slug in SOCIAL else None


def common(path, page):
    page = {**page, 'og_image': page.get('og_image') or og_image(page)}
    return {'page': page, 'canonical': canonical(path), 'nav': nav_for(path), 'asset_v': ASSET_V,
            'is_home': path == '', 'tools': TOOLS, 'tool_by_key': TOOL_BY_KEY, 'pages': PAGES}


def render_article(path):
    p = PAGES[path]
    label, href = SECTIONS[p['section']]
    body = (ROOT / 'content_pages' / f"{p['slug']}.html").read_text(encoding='utf-8')
    tool = TOOL_BY_KEY.get(p['tool']) if p.get('tool') else None
    side = [tool] if tool else []
    side += [t for t in TOOLS if t['flagship'] and t not in side][:3 - len(side)]
    related = [q for q in PAGES.values() if q['section'] == p['section'] and q['path'] != path][:4]
    ctx = common(path, {**p, 'jsonld': p.get('jsonld', [])})
    ctx.update({'section': {'label': label, 'href': href}, 'body': body, 'tool': tool, 'side_tools': side,
                'related': related, 'lead_segment': 'arbetsgivare' if p['section'] in ('arbetsgivare', 'mall') else 'individ'})
    return env.get_template('article.html').render(**ctx)


def render_tool(path):
    t = TOOL_BY_PATH[path]
    tpl = f"tools/{t['key']}.html"
    meta = TOOL_META.get(t['key'], {})
    page = {'title': meta.get('title', f"{t['name']} | Neurovibe"), 'description': meta.get('description', t['summary']),
            'slug': t['key'], 'jsonld': [json.dumps({
                '@context': 'https://schema.org', '@type': 'WebApplication', 'name': t['name'], 'url': canonical(path),
                'applicationCategory': 'BusinessApplication', 'operatingSystem': 'Webbläsare', 'inLanguage': 'sv-SE',
                'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'SEK'}, 'description': t['summary']}, ensure_ascii=False)]}
    ctx = common(path, page)
    ctx.update({'tool': t, 'lead_segment': 'arbetsgivare' if t['for'] == 'Chef och HR' else 'individ'})
    return env.get_template(tpl).render(**ctx)


def render_hub(path):
    tpl, meta = HUBS[path]
    page = {'slug': path.replace('.html', '') or 'start', 'jsonld': [], **meta}
    ctx = common(path, page)
    ctx.update({'guides': [p for p in PAGES.values() if p['section'] in ('guide', 'medarbetare', 'data', 'stod', 'arbetsgivare')],
                'templates_list': [p for p in PAGES.values() if p['section'] == 'mall'],
                'flagships': [t for t in TOOLS if t['flagship']], 'more_tools': [t for t in TOOLS if not t['flagship']],
                'lead_segment': 'arbetsgivare' if path == 'arbetsgivarpaketet.html' else 'individ'})
    if path == '':
        ctx['page']['jsonld'] = [json.dumps({'@context': 'https://schema.org', '@type': 'WebSite', 'name': 'Neurovibe',
                                             'url': SITE + '/', 'inLanguage': 'sv-SE'}, ensure_ascii=False)]
    return env.get_template(tpl).render(**ctx)


def render_404():
    ctx = common('404', {'title': 'Sidan finns inte | Neurovibe', 'noindex': True, 'jsonld': [], 'slug': '404'})
    ctx.update({'flagships': [t for t in TOOLS if t['flagship']]})
    return env.get_template('hubs/404.html').render(**ctx)


TOOL_META = {
    'anpassningsplanen': {'title': 'Anpassningsplanen – underlag om anpassningar på jobbet vid ADHD och autism | Neurovibe',
                          'description': 'Beskriv vad som tar energi och vad som hjälper. Få ett färdigt underlag om anpassningar enligt AFS 2023:2 att gå igenom med din chef. Gratis, ingen inloggning.'},
    'stodkollen': {'title': 'Stödkollen – vilket stöd kan du få vid ADHD eller autism? | Neurovibe',
                   'description': 'Svara på några frågor och se vilka stöd från Arbetsförmedlingen och Försäkringskassan som kan gälla dig: lönebidrag, arbetshjälpmedel, SIUS, aktivitetsersättning med mera.'},
    'atergangsplanen': {'title': 'Plan för återgång i arbete – mall och tidsfrister | Neurovibe',
                        'description': 'Gör arbetsgivarens plan för återgång i arbete i Försäkringskassans struktur. Räknar ut dag 30 och dag 60 och ger dig en plan att skriva ut.'},
    'fokustimern': {'title': 'Fokustimer – pomodoro och body doubling på svenska | Neurovibe',
                    'description': 'En lugn pomodoro-timer på svenska: välj passlängd, se tiden som en yta som krymper och ta pauser som blir av. Med läge för body doubling.'},
    'schema-generatorn': {'title': 'Veckoschema för ADHD och autism – bygg en hållbar arbetsvecka | Neurovibe',
                          'description': 'Bygg ett veckoschema som balanserar fokustid, möten och återhämtning vid ADHD eller autism. Skriv ut eller spara som PDF.'},
    'belastningskollen': {'title': 'Belastningskollen – väg belastning mot återhämtning | Neurovibe',
                          'description': 'Se hur sensorisk belastning, kognitiva krav, sömn och maskering väger mot varandra – och vad du kan ändra först.'},
    'motesguiden': {'title': 'Inkluderande möten – checklista och agendamall | Neurovibe',
                    'description': 'Checklista för möten som tar mindre energi vid NPF: före, under och efter mötet. Med agendamall att skriva ut.'},
    'nedbrytaren': {'title': 'Uppgiftsnedbrytaren – dela upp en uppgift som känns för stor | Neurovibe',
                    'description': 'Kommer du inte igång? Dela upp uppgiften i tre små steg där det första tar under fem minuter.'},
    'intervjuguiden': {'title': 'Intervjuguide för neurodivergenta kandidater | Neurovibe',
                       'description': 'Bygg en intervju som mäter kompetens i stället för förmågan att småprata: frågor i förväg, tydlig struktur och skriftliga alternativ.'},
    'ai-kalkylatorn': {'title': 'Tidskalkylator – hur mycket tid kan stödverktyg frigöra? | Neurovibe',
                       'description': 'Räkna ut hur mycket tid planering, mejl och möten tar i veckan – och hur mycket stödverktyg kan frigöra.'},
}


def resolve(path):
    """Return rendered HTML for a site path ('' = home, 'x.html', 'arbetsgivarpaketet/y.html') or None."""
    path = path.lstrip('/')
    if path == 'index.html':
        path = ''
    if path in HUBS:
        return render_hub(path)
    if path in TOOL_BY_PATH:
        return render_tool(path)
    if path in PAGES:
        return render_article(path)
    return None


def sitemap_xml():
    today = date.today().isoformat()
    urls = [('', today, '1.0')]
    urls += [(t['path'], today, '0.9' if t['flagship'] else '0.7') for t in TOOLS]
    urls += [(h, today, '0.8') for h in ('verktyg.html', 'resurser.html', 'arbetsgivarpaketet.html')]
    urls += [(p['path'], p.get('updated') or today, '0.6') for p in PAGES.values() if not p.get('noindex')]
    seen, out = set(), []
    for loc, mod, prio in urls:
        if loc in seen:
            continue
        seen.add(loc)
        out.append(f'  <url><loc>{canonical(loc)}</loc><lastmod>{mod}</lastmod><priority>{prio}</priority></url>')
    return '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(out) + '\n</urlset>\n'
