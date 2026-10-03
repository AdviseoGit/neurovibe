/* Återgångsplanen — a return-to-work plan with dates computed from the first sick day.
   Milestones (FK): plan ready by day 30 when the absence is expected to last ≥ 60 days;
   after day 90 and day 180 the assessment basis widens. Checked against forsakringskassan.se 2026-10-03. */
(function () {
  "use strict";
  var D = window.nvDoc;
  var ATGARDER = [
    ["uppgifter", "Anpassade arbetsuppgifter", "Arbetsuppgifterna ändras eller begränsas under en period."],
    ["tider", "Anpassade arbetstider", "Kortare dagar, senare start eller fler pauser."],
    ["plats", "Anpassad arbetsplats", "Lugnare plats, möjlighet att arbeta hemifrån vissa dagar."],
    ["belastning", "Minskad arbetsbelastning", "Färre ärenden samtidigt och tydliga prioriteringar."],
    ["stod", "Stöd att hantera stress och planering", "Regelbundna avstämningar, struktur för veckan, stödsamtal."],
    ["hjalpmedel", "Hjälpmedel", "Till exempel brusreducerande hörlurar eller planeringsverktyg."],
    ["fhv", "Företagshälsovård eller annan rehabiliteringstjänst", "Bedömning, samtalsstöd eller arbetsplatsbesök."],
    ["utbildning", "Utbildning eller omskolning", "Om det behövs för att kunna gå tillbaka till arbetet eller till andra uppgifter."]
  ];
  var box = document.getElementById("atgarder");
  box.innerHTML = '<legend class="visually-hidden">Åtgärder</legend>' + ATGARDER.map(function (a) {
    return '<label class="option"><input type="checkbox" name="atgard" value="' + a[0] + '"><span><span class="t">' + a[1] + '</span><span class="d">' + a[2] + "</span></span></label>";
  }).join("");
  var BY = {}; ATGARDER.forEach(function (a) { BY[a[0]] = a; });

  function milestones(a) {
    if (!a.start) return [];
    return [
      [D.addDays(a.start, 29), "Dag 30", a.langd === "nej" ? "Planen är inget krav när sjukskrivningen väntas vara kortare än 60 dagar – men bra att ha." : "Planen för återgång ska vara klar."],
      [D.addDays(a.start, 89), "Dag 90", "Därefter prövas sjukpenningen mot andra uppgifter hos arbetsgivaren eller arbete med anpassning."],
      [D.addDays(a.start, 179), "Dag 180", "Därefter bedöms arbetsförmågan mot hela arbetsmarknaden."]
    ];
  }

  function ramp(a) {
    if (!a.borjan) return [];
    var g = +(a.startgrad || 50), step = +(a.steg || 21), d = a.borjan, rows = [];
    while (g < 100) { rows.push([d, g]); d = D.addDays(d, step); g = Math.min(100, g + 25); }
    rows.push([d, 100]);
    return rows;
  }

  function renderLive(a) {
    var ms = milestones(a);
    document.getElementById("live").innerHTML = ms.length
      ? "<ul style='list-style:none;margin:0;padding:0;display:grid;gap:10px'>" + ms.map(function (m) {
          return "<li><span style='display:block;font-size:13px;color:var(--muted)'>" + m[1] + "</span><strong style='font-weight:600'>" + D.fmt(m[0]) + "</strong></li>";
        }).join("") + "</ul>"
      : "<p style='margin:0;color:var(--muted)'>Fyll i första sjukdagen så räknas datumen ut.</p>";
  }

  function para(t) { return t ? "<p>" + D.esc(t).replace(/\n/g, "<br>") + "</p>" : "<p style='color:var(--muted)'>[Fylls i tillsammans med medarbetaren]</p>"; }

  function renderDoc(a) {
    var ms = milestones(a), r = ramp(a);
    var chosen = (a.atgard || []).map(function (k) { return BY[k]; }).filter(Boolean);
    var extra = (a.ovrigt || "").split("\n").map(function (s) { return s.trim(); }).filter(Boolean);
    var due = a.start ? D.addDays(a.start, 29) : D.today();
    var html = "<h2>Plan för återgång i arbete</h2>" +
      '<p class="doc-meta">Upprättad ' + D.fmt(D.today()) + (a.namn ? " · Medarbetare: " + D.esc(a.namn) : "") + (a.ansvarig ? " · Ansvarig chef: " + D.esc(a.ansvarig) : "") + "</p>" +
      "<h3>Sjukskrivningen</h3><p>Första sjukdag: " + (a.start ? D.fmt(a.start) : "[datum]") + ". " +
      ({ ja: "Sjukskrivningen väntas pågå minst 60 dagar.", nej: "Sjukskrivningen väntas vara kortare än 60 dagar.", "vet-ej": "Det är ännu inte klart hur länge sjukskrivningen pågår." }[a.langd] || "") + "</p>" +
      "<h3>Arbetsuppgifter</h3>" + para(a.uppgifter) +
      "<h3>Det som behöver förändras</h3>" + para(a.hinder) +
      "<h3>Det medarbetaren kan göra nu</h3>" + para(a.formaga) +
      "<h3>Åtgärder</h3>" +
      ((chosen.length || extra.length) ? "<table><thead><tr><th scope='col'>Åtgärd</th><th scope='col'>Ansvarig</th><th scope='col'>Klart senast</th></tr></thead><tbody>" +
        chosen.map(function (c) { return "<tr><td><strong style='font-weight:600'>" + c[1] + ".</strong> " + c[2] + "</td><td>" + (D.esc(a.ansvarig) || "Chef") + "</td><td>" + D.fmt(due) + "</td></tr>"; }).join("") +
        extra.map(function (e) { return "<tr><td>" + D.esc(e) + "</td><td>" + (D.esc(a.ansvarig) || "Chef") + "</td><td>" + D.fmt(due) + "</td></tr>"; }).join("") +
        "</tbody></table>" : "<p style='color:var(--muted)'>[Inga åtgärder valda]</p>") +
      "<h3>Upptrappning</h3>" +
      (r.length ? "<table><thead><tr><th scope='col'>Från och med</th><th scope='col'>Omfattning</th></tr></thead><tbody>" +
        r.map(function (x) { return "<tr><td>" + D.fmt(x[0]) + "</td><td>" + x[1] + " procent</td></tr>"; }).join("") + "</tbody></table>"
        : "<p style='color:var(--muted)'>[Datum för start bestäms tillsammans]</p>") +
      "<h3>Kontakt under sjukskrivningen</h3><p>Chef och medarbetare har kontakt " + (a.kontakt || "varje vecka") + " via " + (a.kanal || "kort telefonsamtal") + ". Medarbetaren bestämmer hur mycket som berättas om hälsan.</p>" +
      (ms.length ? "<h3>Tidsgränser att hålla koll på</h3><ul>" + ms.map(function (m) { return "<li><strong style='font-weight:600'>" + m[1] + " (" + D.fmt(m[0]) + ").</strong> " + m[2] + "</li>"; }).join("") + "</ul>" : "") +
      "<h3>Uppföljning</h3><p>Planen följs upp vid varje kontakt och ändras när något förändras. Nästa gemensamma genomgång: " + D.fmt(D.addDays(D.today(), 14)) + ".</p>" +
      '<div class="sign"><div>Medarbetare</div><div>Chef</div></div>';
    document.getElementById("doc").innerHTML = html;
  }

  var form = document.querySelector('[data-stepper="atergangsplanen"]');
  var stepper = window.nvStepper(form, {
    validate: function (step, a) { if (step === 0 && !a.start) return "Fyll i första sjukdagen – den behövs för datumen."; if (step === 2 && !(a.atgard || []).length && !(a.ovrigt || "").trim()) return "Välj minst en åtgärd eller skriv en egen."; return null; },
    onStep: function (step, a) { renderLive(a); if (step === 4) { renderDoc(a); if (window.nv) window.nv.usage("atergangsplanen", { done: true }); } },
    onChange: function (step, a) { renderLive(a); if (step === 4) renderDoc(a); }
  });
  document.getElementById("copy-doc").addEventListener("click", function (e) { D.copyText(document.getElementById("doc"), e.target); });
  renderLive(stepper.data());
})();
