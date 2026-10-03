"""Click through every tool in a real browser against a running server and assert the output.
    python3 tools_build/e2e_tools.py [base]   (default http://localhost:8099)
Exits non-zero on the first failure; also fails on any console error or uncaught page error."""
import sys
from playwright.sync_api import sync_playwright, expect

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'http://localhost:8099').rstrip('/')
errors = []


def page_for(browser, path, width=1440):
    ctx = browser.new_context(viewport={'width': width, 'height': 900}, locale='sv-SE')
    p = ctx.new_page()
    p.on('pageerror', lambda e: errors.append(f'{path}: pageerror {e}'))
    p.on('console', lambda m: m.type == 'error' and 'googletagmanager' not in m.text and errors.append(f'{path}: console {m.text}'))
    p.goto(BASE + path)
    return p


def ok(msg):
    print('  ok  ', msg)


with sync_playwright() as pw:
    b = pw.chromium.launch()

    # --- Anpassningsplanen: full flow + reload resumes on last step
    p = page_for(b, '/verktyg-anpassningsgenerator.html')
    p.get_by_role('button', name='Nästa: Vad tar energi').click()
    p.get_by_role('button', name='Nästa: Vad som hjälper').click()
    expect(p.locator('[data-step="1"] [data-error]')).to_be_visible(); ok('anpassning: kräver minst ett område')
    for t in ('Ljud och intryck', 'Avbrott mitt i en uppgift', 'Att komma igång och planera'):
        p.locator('#areas label', has_text=t).click()
    expect(p.locator('#areas input[value="tid"]')).to_be_disabled(); ok('anpassning: max tre områden')
    p.get_by_role('button', name='Nästa: Vad som hjälper').click()
    p.locator('#helps label', has_text='Hörlurar med brusreducering').click()
    p.fill('#egen', 'Jag gör mitt bästa arbete före lunch.')
    p.get_by_role('button', name='Nästa: Förslag att ta upp').click()
    p.get_by_role('button', name='Visa mitt underlag').click()
    doc = p.locator('#doc')
    expect(doc).to_contain_text('Underlag inför samtal om arbetsanpassning')
    expect(doc).to_contain_text('Ljud och intryck')
    expect(doc).to_contain_text('Hörlurar med brusreducering')
    expect(doc).to_contain_text('före lunch')
    expect(doc).to_contain_text('AFS 2023:2'); ok('anpassning: dokument byggt med val, hjälp och egen text')
    n_rows = doc.locator('tbody tr').count(); assert n_rows >= 3, n_rows; ok(f'anpassning: {n_rows} förslag i tabellen')
    p.reload()
    expect(p.locator('#doc')).to_contain_text('Hörlurar med brusreducering'); ok('anpassning: återupptas efter omladdning')
    p.get_by_role('button', name='Börja om').first.click()
    expect(p.get_by_role('heading', name='Vem fyller i?')).to_be_visible(); ok('anpassning: börja om')

    # --- Stödkollen: söker jobb, 19–29, nedsatt länge, inskriven + underlag
    p = page_for(b, '/verktyg-myndighetsnavigator.html')
    p.locator('label', has_text='Jag söker jobb').click(); p.get_by_role('button', name='Nästa: Ålder').click()
    p.locator('label', has_text='19–29 år').click(); p.get_by_role('button', name='Nästa: Arbetsförmåga').click()
    p.locator('label', has_text='Mindre än heltid – och det har varat').click(); p.get_by_role('button', name='Nästa: Behov').click()
    for t in ('Jag är inskriven på Arbetsförmedlingen', 'Jag har ett intyg', 'Jag behöver stöd för att lära mig'):
        p.locator('label', has_text=t).click()
    p.get_by_role('button', name='Visa mitt resultat').click()
    res = p.locator('#results')
    for name in ('Lönebidrag', 'SIUS', 'Aktivitetsersättning', 'Bidrag till hjälpmedel på arbetsplatsen'):
        expect(res).to_contain_text(name)
    expect(res).not_to_contain_text('Sjukersättning')
    expect(p.locator('#next')).to_contain_text('handläggare'); ok('stödkollen: söker jobb 19–29 → lönebidrag, SIUS, aktivitetsersättning, AF-hjälpmedel')
    assert res.locator('a[href^="https://"]').count() >= 4; ok('stödkollen: källänkar till myndigheter')
    # sjukskriven 30–64
    p.get_by_role('button', name='Börja om').first.click()
    p.locator('label', has_text='Jag är sjukskriven från mitt jobb').click(); p.get_by_role('button', name='Nästa: Ålder').click()
    p.locator('label', has_text='30–64 år').click(); p.get_by_role('button', name='Nästa: Arbetsförmåga').click()
    p.locator('label', has_text='Jag kan inte arbeta alls').click(); p.get_by_role('button', name='Nästa: Behov').click()
    p.get_by_role('button', name='Visa mitt resultat').click()
    expect(res).to_contain_text('Plan för återgång i arbete'); expect(res).to_contain_text('Sjukersättning')
    expect(res).to_contain_text('Bidrag till arbetshjälpmedel (Försäkringskassan)')
    expect(p.locator('#next')).to_contain_text('plan för återgång'); ok('stödkollen: sjukskriven 30–64 → återgång, sjukersättning, FK-hjälpmedel')

    # --- Återgångsplanen: dates from first sick day
    p = page_for(b, '/verktyg-atergangsplan.html')
    p.get_by_role('button', name='Nästa: Arbetet i dag').click()
    expect(p.locator('[data-step="0"] [data-error]')).to_be_visible(); ok('återgång: kräver första sjukdag')
    p.fill('#namn', 'A. B.'); p.fill('#start', '2026-09-01'); p.locator('label', has_text='Ja').first.click()
    expect(p.locator('#live')).to_contain_text('30 september 2026'); ok('återgång: dag 30 = 30 september')
    p.get_by_role('button', name='Nästa: Arbetet i dag').click()
    p.fill('#uppgifter', 'Handläggning av ärenden')
    p.get_by_role('button', name='Nästa: Åtgärder').click()
    p.locator('label', has_text='Anpassade arbetstider').click()
    p.get_by_role('button', name='Nästa: Upptrappning').click()
    p.fill('#borjan', '2026-10-15')
    p.get_by_role('button', name='Visa planen').click()
    d = p.locator('#doc')
    for t in ('Plan för återgång i arbete', 'A. B.', 'Anpassade arbetstider', '50 procent', '100 procent', 'Dag 90', '29 november 2026', 'Dag 180', '27 februari 2027'):
        expect(d).to_contain_text(t)
    ok('återgång: plan med åtgärd, upptrappning 50→100, dag 90 = 29 nov, dag 180 = 27 feb 2027')

    # --- small tools
    p = page_for(b, '/verktyg-fokus-timer.html')
    p.locator('label', has_text='15 min fokus').click(); expect(p.locator('#clock')).to_have_text('15:00')
    p.get_by_role('button', name='Starta').click(); p.wait_for_timeout(2200)
    t = p.locator('#clock').inner_text(); assert t < '15:00', t
    p.get_by_role('button', name='Pausa').click(); ok(f'fokustimer: räknar ner ({t}) och pausar')

    for path, btn, expect_text in [
        ('/verktyg-inkluderande-moten.html', 'Visa checklistan', 'Före mötet'),
        ('/intervju-guide.html', 'Skapa intervjuplanen', 'Rättvis bedömning'),
        ('/verktyg-schema-generator.html', 'Skapa veckoschemat', 'Måndag'),
        ('/verktyg-burnout-kalkylator.html', 'Visa min balans', 'Din balans just nu'),
        ('/verktyg-nedbrytare.html', 'Dela upp uppgiften', 'Tre steg för'),
        ('/ai-verktyg-jobb-kalkylator.html', 'Räkna', 'timmar i veckan'),
    ]:
        p = page_for(b, path)
        p.get_by_role('button', name=btn).click()
        expect(p.locator('#out')).to_contain_text(expect_text); ok(f'{path}: {expect_text}')

    # --- home router + reading settings + consent + lead form (no submit)
    p = page_for(b, '/')
    p.select_option('#mal', 'verktyg-atergangsplan.html'); p.get_by_role('button', name='Visa mitt nästa steg').click()
    p.wait_for_url('**/verktyg-atergangsplan.html'); ok('startsida: väljaren leder rätt')
    p.goto(BASE + '/lagkrav-anpassningar-arbetsmiljo.html')
    p.get_by_role('button', name='Läsinställningar').click(); p.get_by_label('Större text').check()
    assert 'rs-large' in p.locator('body').get_attribute('class'); p.reload()
    assert 'rs-large' in (p.locator('body').get_attribute('class') or ''); ok('läsinställningar: sparas')
    expect(p.locator('#consent')).to_be_visible(); p.get_by_role('button', name='Nej tack').click()
    expect(p.locator('#consent')).to_be_hidden(); ok('samtycke: kan avböjas')
    assert p.locator('form[data-nv-lead]').count() == 1; ok('artikel: leadformulär finns')

    # --- mobile width: no horizontal scroll on key pages
    for path in ('/', '/verktyg-anpassningsgenerator.html', '/verktyg-myndighetsnavigator.html', '/forsakringskassan-arbetsformedlingen-stod.html', '/arbetsgivarpaketet.html'):
        p = page_for(b, path, width=390)
        sw = p.evaluate('document.documentElement.scrollWidth'); cw = p.evaluate('document.documentElement.clientWidth')
        assert sw <= cw + 1, f'{path} overflows at 390px: {sw} > {cw}'
    ok('mobil 390 px: ingen horisontell scroll på nyckelsidor')
    b.close()

if errors:
    print('\nFEL I WEBBLÄSAREN:'); print('\n'.join(errors)); sys.exit(1)
print('\nALLA VERKTYGSTESTER GRÖNA')
