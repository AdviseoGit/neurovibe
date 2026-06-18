RAPPORT — neurovibe.se 2026-06-17
SCORECARD: SEO 1 klick senaste 28, plats 1.9 | Leadflow Fungerande nu via /api/waitlist | Design/UX Åtgärdat gray-50 till dark theme | Teknik Next.js/FastAPI fungerar | Data-tillgång leads sparas nu i waitlist.txt
SAJTREVIEW: Verktygen och "Fördelarna" m.fl. hade bg-gray-50/white istället för sajtens mörka nordstjärna (bg-[#050505]). Header/footer saknades på verktygen. Åtgärdat så designen är 100% konsekvent mörk + integrerad nav.
DESIGN: Tog bort all "design-skuld" gällande ljusa teman på artiklar och verktyg. Nu är allt i mörkt läge med gemensam nav och footer.
FÄRSKHET: Uppdaterade inte specifikt idag förutom verktygsfunktionalitetens integration med sajtens design och waitlist.
PROGRESSION: Verktygen (Milstolpe 2) har nu en fullt integrerad front-end i samma design som resten av sajten, och data-capture back-end fungerar och lagrar e-post. Checkbox för verktygens enhetliga stilmall är ikryssad.
VAL: Högsta ROI-drag var att a) eliminera design-avvikelserna (bg-gray) för att bygga ett trovärdigt varumärke och b) implementera `/api/waitlist` backend för att *faktiskt* kunna fånga data, istället för falska form-actions.
ÅTGÄRD: Fixat färgkoder/css-klasser i verktygen, adderat gemensam header/footer i verktygen, och lagt till en `Form` POST-endpoint i FastAPI som lagrar data.
NÅR MÅLGRUPPEN VIA: Konsekvent och snygg design bygger trust, att faktiskt kunna anmäla sig ökar leadflow.
DATA-ÄGANDE: Datamoaten är nu startad. Endpoint `/api/waitlist` tar emot email-adresser (och leder till `waitlist-success.html`) som lagras i `leads/waitlist.txt`.
PUBLICERAT: JA | commit 535a023 | live 200 + visar innehåll: ja https://neurovibe.se/verktyg-fokus-timer.html
INTEGRERAT: länkad ja (i nav och footer) | sitemap ja
INFRA: Leadflow FIXAT | GA4 G-YJG1D5GJPR finns | GSC data: ja
MOBIL: FIXAT (nav fungerar med hamburger-menyn från det uppdaterade skriptet)
FIXAT: Trasiga backend-paths (importer och filvägar) åtgärdade (500 Error löst till 303 Redirect).
PIVOT: Fortsätter kursen, bygga vidare på verktygens logik så att insats -> output lagras (t.ex burnout-kalkylator).
NÄSTA: Koppla burnout-kalkylatorn och uppgiftsnedbrytaren till en backend-endpoint som sparar anonymiserad input för att aggregera "Neuro-data" inför framtida rapport.
