/* Stödkollen — a small, explicit rules engine. Every rule and figure below comes from the
   authority's own page (linked in `src`) and was checked on CHECKED. When a rule changes,
   change it here and bump CHECKED; nothing is generated. */
(function () {
  "use strict";
  var CHECKED = "2026-10-03";
  var D = window.nvDoc;

  var SRC = {
    afsAnpassning: ["Arbetsmiljöverket – AFS 2023:2", "https://www.av.se/arbetsmiljoarbete-och-inspektioner/publikationer/foreskrifter/beslutade-foreskrifter-som-trader-i-kraft-2025/afs-20232/"],
    lonebidrag: ["Arbetsförmedlingen – Lönebidrag", "https://arbetsformedlingen.se/for-arbetsgivare/anstallningsstod/stod-nar-en-person-har-en-funktionsnedsattning/lonebidrag"],
    hjalpmedelAf: ["Arbetsförmedlingen – Bidrag till hjälpmedel på arbetsplatsen", "https://arbetsformedlingen.se/for-arbetsgivare/anstallningsstod/stod-nar-en-person-har-en-funktionsnedsattning/bidrag-till-hjalpmedel-pa-arbetsplatsen"],
    hjalpmedelFk: ["Försäkringskassan – Arbetshjälpmedel", "https://www.forsakringskassan.se/privatperson/vuxen-med-funktionsnedsattning/arbetshjalpmedel"],
    sius: ["Arbetsförmedlingen – SIUS", "https://arbetsformedlingen.se/for-arbetsgivare/kom-igang-med-din-rekrytering/fa-stod-i-rekryteringen/sarskild-stodperson-for-introduktions--och-uppfoljningsstod-sius"],
    aktivitet: ["Försäkringskassan – Aktivitetsersättning", "https://www.forsakringskassan.se/privatperson/vuxen-med-funktionsnedsattning/aktivitetsersattning-for-unga-vuxna"],
    sjukersattning: ["Försäkringskassan – Sjukersättning", "https://www.forsakringskassan.se/privatperson/funktionsnedsattning/sjukersattning/sjukersattning-vid-stadigvarande-nedsatt-arbetsformaga"],
    atergang: ["Försäkringskassan – Om din medarbetare är sjuk länge", "https://www.forsakringskassan.se/arbetsgivare/sjukdom-och-skada/om-din-medarbetare-ar-sjuk-lange"]
  };

  function has(list, v) { return (list || []).indexOf(v) !== -1; }

  /* Each rule returns null (not shown) or {status: yes|maybe|no, why:[...], check:[...]} */
  var RULES = [
    { id: "anpassning", name: "Anpassning av arbetet hos arbetsgivaren", src: SRC.afsAnpassning,
      what: "Arbetsgivaren ska utreda behovet av anpassning, göra det som behövs och följa upp. Det kan gälla arbetstider, arbetsuppgifter, arbetsplats, hjälpmedel och hur arbetet leds.",
      amount: "Ingen ansökan – det är arbetsgivarens skyldighet. Ingen diagnos krävs.",
      run: function (a) {
        if (a.sit === "soker") return null;
        return { status: "yes", why: ["Du har en anställning, och anpassningsskyldigheten gäller alla anställda."],
          check: ["Gör ett underlag med Anpassningsplanen och boka ett samtal med din chef."] };
      } },
    { id: "atergang", name: "Plan för återgång i arbete", src: SRC.atergang,
      what: "När en sjukskrivning väntas vara minst 60 dagar ska arbetsgivaren ha en plan för återgång i arbete klar senast dag 30.",
      amount: "Ingen ersättning – en skyldighet för arbetsgivaren.",
      run: function (a) {
        if (a.sit !== "sjuk") return null;
        return { status: "yes", why: ["Du är sjukskriven från ditt jobb."],
          check: ["Fråga om sjukskrivningen väntas vara minst 60 dagar – då ska planen finnas senast dag 30."] };
      } },
    { id: "hjalpmedel-af", name: "Bidrag till hjälpmedel på arbetsplatsen (Arbetsförmedlingen)", src: SRC.hjalpmedelAf,
      what: "Bidrag till hjälpmedel som behövs på grund av funktionsnedsättningen, när du är ny på jobbet eller söker jobb.",
      amount: "Högst 100 000 kronor per år.",
      run: function (a) {
        if (a.sit !== "anst-ny" && a.sit !== "soker") return null;
        var need = has(a.behov, "hjalpmedel");
        return { status: need ? "yes" : "maybe",
          why: [a.sit === "anst-ny" ? "Du har varit anställd i 12 månader eller kortare – då är det Arbetsförmedlingen som handlägger." : "Du söker jobb.",
            need ? "Du har angett att du behöver hjälpmedel." : "Du har inte angett att du behöver hjälpmedel – men kan ha nytta av att fråga."],
          check: ["Behovet ska anmälas under anställningens första 12 månader."] };
      } },
    { id: "hjalpmedel-fk", name: "Bidrag till arbetshjälpmedel (Försäkringskassan)", src: SRC.hjalpmedelFk,
      what: "Bidrag till hjälpmedel som behövs för att du ska kunna arbeta, när du har varit anställd längre än 12 månader.",
      amount: "Hälften av kostnaden. Arbetsgivaren betalar alltid de första 10 000 kronorna själv, och bidraget är högst 50 000 kronor.",
      run: function (a) {
        if (a.sit !== "anst-lang" && a.sit !== "sjuk") return null;
        var need = has(a.behov, "hjalpmedel");
        return { status: need ? "yes" : "maybe",
          why: ["Du har en anställning sedan längre tid – då är det Försäkringskassan som handlägger.",
            need ? "Du har angett att du behöver hjälpmedel." : "Du har inte angett att du behöver hjälpmedel."],
          check: ["Hjälpmedlet ska gå utöver det arbetsgivaren normalt ska ordna på en arbetsplats."] };
      } },
    { id: "lonebidrag", name: "Lönebidrag", src: SRC.lonebidrag,
      what: "Ett bidrag till arbetsgivaren för din lön när en funktionsnedsättning sänker arbetsförmågan i det jobb du har eller söker.",
      amount: "Räknas på lön upp till 20 000 kronor i månaden vid heltid, i förhållande till hur mycket arbetsförmågan är nedsatt. Längst fyra år, i perioder om högst ett år i taget.",
      run: function (a) {
        if (a.formaga === "inte") return null;
        var inskriven = has(a.behov, "inskriven"), underlag = has(a.behov, "underlag");
        var reduced = a.formaga !== "heltid";
        var why = [], check = [];
        var status = "maybe";
        if (a.sit === "soker" && inskriven && underlag) status = "yes";
        if (a.formaga === "heltid") why.push("Du klarar heltid med anpassningar – lönebidrag kan ändå bli aktuellt om du hinner mindre än andra i samma jobb.");
        if (reduced) why.push("Din arbetsförmåga är nedsatt i förhållande till heltid.");
        if (inskriven) why.push("Du är inskriven på Arbetsförmedlingen."); else check.push("Du behöver vara inskriven på Arbetsförmedlingen.");
        if (underlag) why.push("Du har underlag om funktionsnedsättningen."); else check.push("Arbetsförmedlingen behöver underlag som visar funktionsnedsättningen.");
        if (a.sit !== "soker") check.push("Har du redan ett jobb: fråga din handläggare om lönebidrag för den anställning du har.");
        return { status: status, why: why, check: check };
      } },
    { id: "sius", name: "SIUS – särskild stödperson vid introduktion och uppföljning", src: SRC.sius,
      what: "En konsulent från Arbetsförmedlingen som hjälper dig att lära in arbetsuppgifterna och följer upp när du har börjat.",
      amount: "Kostar inget för dig eller arbetsgivaren. Introduktion i högst sex månader, uppföljning i minst tolv månader.",
      run: function (a) {
        if (a.sit !== "soker" && a.sit !== "anst-ny") return null;
        var need = has(a.behov, "inlarning"), inskriven = has(a.behov, "inskriven");
        return { status: need && inskriven ? "yes" : "maybe",
          why: [a.sit === "soker" ? "Du söker jobb." : "Du är ny på jobbet.",
            need ? "Du har angett att du behöver stöd för att lära in arbetsuppgifterna." : "Du har inte angett att du behöver stöd vid inlärning."],
          check: inskriven ? [] : ["Du behöver vara inskriven på Arbetsförmedlingen."] };
      } },
    { id: "aktivitet", name: "Aktivitetsersättning", src: SRC.aktivitet,
      what: "Ersättning från Försäkringskassan för dig som är 19–29 år och inte kan arbeta heltid på grund av sjukdom, skada eller funktionsnedsättning.",
      amount: "Arbetsförmågan ska vara nedsatt med minst en fjärdedel i minst ett år. Fyra nivåer, från en fjärdedel till hel. Högst tre år i taget.",
      run: function (a) {
        if (a.alder !== "19-29") {
          if (a.formaga === "lagre-lang" || a.formaga === "inte") return { status: "no", why: ["Aktivitetsersättning gäller bara dig som är 19–29 år."], check: [] };
          return null;
        }
        if (a.formaga === "lagre-lang" || a.formaga === "inte") return { status: "maybe",
          why: ["Du är 19–29 år.", a.formaga === "inte" ? "Du kan inte arbeta just nu." : "Din arbetsförmåga är nedsatt sedan länge eller väntas vara det."],
          check: ["Försäkringskassan bedömer om nedsättningen är minst en fjärdedel i minst ett år – det krävs ett läkarutlåtande."] };
        if (a.formaga === "lagre-kort") return { status: "no", why: ["Nedsättningen väntas gå över – aktivitetsersättning kräver minst ett år."], check: [] };
        return null;
      } },
    { id: "sjukersattning", name: "Sjukersättning", src: SRC.sjukersattning,
      what: "Ersättning från Försäkringskassan när arbetsförmågan är nedsatt för all överskådlig framtid.",
      amount: "Arbetsförmågan ska vara nedsatt med minst en fjärdedel för all överskådlig framtid och i alla typer av arbeten. Fyra nivåer.",
      run: function (a) {
        if (a.alder !== "30-64") return null;
        if (a.formaga === "inte" || a.formaga === "lagre-lang") return { status: "maybe",
          why: ["Din arbetsförmåga är nedsatt sedan länge eller helt."],
          check: ["Kravet är högt: nedsättningen ska gälla för all överskådlig framtid och mot alla typer av arbeten. Prata med din läkare först."] };
        return null;
      } }
  ];

  var STATUS = {
    yes: ['chip chip-yes', '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M5 12l4 4 10-10"/></svg>Troligen aktuellt'],
    maybe: ['chip chip-maybe', '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16v.5"/></svg>Kan vara aktuellt'],
    no: ['chip chip-no', '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><path d="M6 12h12"/></svg>Inte aktuellt just nu']
  };
  var ORDER = { yes: 0, maybe: 1, no: 2 };

  function nextStep(a, results) {
    var inskriven = has(a.behov, "inskriven");
    if (a.sit === "sjuk") return ["Be din chef om en plan för återgång i arbete", "Visa Återgångsplanen", "/verktyg-atergangsplan.html"];
    if (a.sit === "soker" && !inskriven) return ["Skriv in dig på Arbetsförmedlingen", "Läs om stödet", "/forsakringskassan-arbetsformedlingen-stod.html"];
    if (a.sit === "soker") return ["Boka ett möte med din handläggare och fråga om lönebidrag och SIUS", "Läs om stödet", "/forsakringskassan-arbetsformedlingen-stod.html"];
    if (has(a.behov, "hjalpmedel")) return ["Prata med din chef om hjälpmedel – arbetsgivaren ansöker om bidraget", "Gör ett underlag", "/verktyg-anpassningsgenerator.html"];
    return ["Gör ett underlag om anpassningar och boka ett samtal med din chef", "Öppna Anpassningsplanen", "/verktyg-anpassningsgenerator.html"];
  }

  function render(a) {
    var res = RULES.map(function (r) { var out = r.run(a); return out ? { r: r, o: out } : null; }).filter(Boolean);
    res.sort(function (x, y) { return ORDER[x.o.status] - ORDER[y.o.status]; });
    var nYes = res.filter(function (x) { return x.o.status !== "no"; }).length;
    document.getElementById("result-title").textContent =
      nYes === 0 ? "Inget stöd ser aktuellt ut just nu" : (nYes === 1 ? "Ett stöd kan vara aktuellt för dig" : nYes + " stöd kan vara aktuella för dig");
    var ns = nextStep(a, res);
    document.getElementById("next").innerHTML = '<div><p class="k">Ditt nästa steg</p><p class="v"><span class="mark">' + ns[0] +
      '</span></p></div><a class="btn no-print" href="' + ns[2] + '">' + ns[1] + "</a>";
    document.getElementById("results").innerHTML = res.map(function (x) {
      var s = STATUS[x.o.status];
      return '<div class="result-card"><div class="top"><h3>' + x.r.name + '</h3><span class="' + s[0] + '">' + s[1] + "</span></div>" +
        '<p style="margin:10px 0 0;color:var(--ink-2)">' + x.r.what + "</p><dl>" +
        "<div><dt>Därför</dt><dd>" + x.o.why.join(" ") + "</dd></div>" +
        (x.o.check.length ? "<div><dt>Att ta reda på</dt><dd>" + x.o.check.join(" ") + "</dd></div>" : "") +
        "<div><dt>Belopp och villkor</dt><dd>" + x.r.amount + "</dd></div></dl>" +
        '<p class="src">Källa: <a href="' + x.r.src[1] + '" rel="noopener" target="_blank">' + x.r.src[0] + "</a> · kontrollerad " + D.fmt(CHECKED) + "</p></div>";
    }).join("");
    document.getElementById("checked").textContent = D.fmt(CHECKED);
    if (window.nv) window.nv.usage("stodkollen", { done: true, sit: a.sit, results: res.map(function (x) { return x.r.id + ":" + x.o.status; }) });
  }

  var LABELS = {
    sit: { "anst-lang": "Jobb > 12 mån", "anst-ny": "Jobb ≤ 12 mån", soker: "Söker jobb", sjuk: "Sjukskriven" },
    alder: { u19: "Under 19", "19-29": "19–29 år", "30-64": "30–64 år", "65": "65+" },
    formaga: { heltid: "Heltid med anpassningar", "lagre-lang": "Mindre än heltid, länge", "lagre-kort": "Mindre än heltid, tillfälligt", inte: "Kan inte arbeta nu" }
  };
  function renderLive(a) {
    var rows = [["Situation", LABELS.sit[a.sit]], ["Ålder", LABELS.alder[a.alder]], ["Arbetsförmåga", LABELS.formaga[a.formaga]]]
      .filter(function (r) { return r[1]; });
    document.getElementById("live").innerHTML = rows.length
      ? "<dl style='margin:0;display:grid;gap:8px'>" + rows.map(function (r) { return "<div><dt style='font-size:13px;color:var(--muted)'>" + r[0] + "</dt><dd style='margin:0;font-weight:500'>" + r[1] + "</dd></div>"; }).join("") + "</dl>"
      : "<p style='margin:0;color:var(--muted)'>Inga svar ännu.</p>";
  }

  var form = document.querySelector('[data-stepper="stodkollen"]');
  var stepper = window.nvStepper(form, {
    validate: function (step, a) {
      if (step === 0 && !a.sit) return "Välj det som stämmer bäst.";
      if (step === 1 && !a.alder) return "Välj en åldersgrupp.";
      if (step === 2 && !a.formaga) return "Välj det som stämmer bäst.";
      return null;
    },
    onStep: function (step, a) { renderLive(a); if (step === 4) render(a); },
    onChange: function (step, a) { renderLive(a); }
  });
  renderLive(stepper.data());
})();
