/* Anpassningsplanen — builds an adaptation plan from a fixed, reviewed library.
   No AI and no network: the same answers always give the same document. */
(function () {
  "use strict";

  var AREAS = [
    { id: "ljud", t: "Ljud och intryck", d: "Öppna kontor, samtal runt omkring, telefoner, starkt ljus, mycket rörelse.",
      doc: "Ljud, samtal och visuella intryck i lokalen tar mycket energi och gör det svårt att hålla fokus.",
      helps: ["Hörlurar med brusreducering", "En lugnare plats för fokusarbete", "Arbeta hemifrån vissa dagar"],
      sugg: [
        ["Brusreducerande hörlurar under hela dagen, utan att det tolkas som ointresse", "enkel"],
        ["Fast plats bort från gångstråk, skrivare och dörrar", "enkel"],
        ["Tillgång till ett tyst rum eller en bokningsbar fokusplats", "medel"],
        ["Möjlighet att arbeta hemifrån vissa dagar för fokusarbete", "medel"]] },
    { id: "avbrott", t: "Avbrott mitt i en uppgift", d: "Någon kommer förbi med en snabb fråga och tråden försvinner.",
      doc: "Avbrott mitt i en uppgift gör att det tar lång tid att komma tillbaka in i arbetet.",
      helps: ["Fasta tider då jag kan störas", "Frågor i chatten i stället för vid skrivbordet", "Stänga av aviseringar"],
      sugg: [
        ["Överenskommet sätt att signalera fokustid (skylt, status i chatten)", "enkel"],
        ["Icke-akuta frågor samlas i chatt eller mejl och besvaras vid fasta tider", "enkel"],
        ["Fasta fokusblock i kalendern som respekteras av teamet", "medel"]] },
    { id: "igang", t: "Att komma igång och planera", d: "Stora uppgifter utan tydlig början, ordning eller delmål.",
      doc: "Stora och otydliga uppgifter är svåra att komma igång med och att dela upp i rätt ordning.",
      helps: ["Uppgifter uppdelade i mindre steg", "En tydlig prioritering", "Korta avstämningar"],
      sugg: [
        ["Större uppgifter delas upp i delmål med datum när de lämnas över", "enkel"],
        ["Tydlig prioritering: vad är viktigast den här veckan", "enkel"],
        ["Korta avstämningar, till exempel tio minuter två gånger i veckan", "medel"],
        ["Ett gemensamt planeringsverktyg där uppgifterna syns", "medel"]] },
    { id: "muntligt", t: "Muntliga instruktioner och minne", d: "Det som sägs på möten eller i förbifarten glöms bort efteråt.",
      doc: "Muntliga instruktioner och beslut på möten är svåra att komma ihåg i efterhand.",
      helps: ["Instruktioner skriftligt", "Anteckningar efter möten", "Checklistor"],
      sugg: [
        ["Viktiga instruktioner och beslut bekräftas skriftligt efteråt", "enkel"],
        ["Mötesanteckningar med vem som gör vad och när", "enkel"],
        ["Checklistor för återkommande arbetsmoment", "enkel"]] },
    { id: "andringar", t: "Oväntade ändringar", d: "Möten som flyttas, nya uppgifter eller ändrade planer utan förvarning.",
      doc: "Oväntade ändringar i schema eller uppgifter skapar stress och tar energi från arbetet.",
      helps: ["Besked i god tid", "En förutsägbar vecka", "En fast kontaktperson"],
      sugg: [
        ["Ändringar meddelas så tidigt som möjligt, och skriftligt", "enkel"],
        ["En förutsägbar veckostruktur med återkommande möten på fasta tider", "medel"],
        ["En fast kontaktperson att fråga när något ändras", "enkel"]] },
    { id: "socialt", t: "Socialt och outtalade regler", d: "Småprat, fika, afterwork, att tolka vad som förväntas.",
      doc: "Sociala situationer och outtalade förväntningar tar energi och skapar osäkerhet.",
      helps: ["Tydliga förväntningar", "Att få avstå från vissa sociala inslag", "Skriftliga svar"],
      sugg: [
        ["Förväntningar på roll och uppgifter uttalas tydligt i stället för att tas för givna", "enkel"],
        ["Frivillighet i sociala aktiviteter utanför arbetsuppgifterna", "enkel"],
        ["Möjlighet att svara skriftligt i stället för spontant på möten", "enkel"]] },
    { id: "tid", t: "Tid och tempo", d: "Svårt att uppskatta tid, deadlines som kommer plötsligt, för mycket samtidigt.",
      doc: "Det är svårt att uppskatta hur lång tid saker tar och att hålla flera uppgifter igång samtidigt.",
      helps: ["Färre parallella uppgifter", "Påminnelser", "Deadlines med marginal"],
      sugg: [
        ["Färre uppgifter igång samtidigt, med tydlig ordning", "enkel"],
        ["Deadlines bestäms tillsammans och med marginal", "enkel"],
        ["Påminnelser i kalendern inför viktiga datum", "enkel"],
        ["Tidshjälpmedel, till exempel en visuell timer eller planeringsprogram", "medel"]] },
    { id: "energi", t: "Energi och återhämtning", d: "Tröttheten kommer plötsligt, dagarna blir för långa eller utan pauser.",
      doc: "Energin räcker inte hela dagen, särskilt när det saknas pauser eller tid att varva ner.",
      helps: ["Kortare pauser under dagen", "Flexibla tider", "Återhämtning efter intensiva moment"],
      sugg: [
        ["Korta pauser för återhämtning under dagen, utan krav på förklaring", "enkel"],
        ["Flexibel start- och sluttid inom överenskomna ramar", "medel"],
        ["Planerad återhämtning efter intensiva moment, till exempel efter långa möten", "enkel"],
        ["Se över arbetstid eller arbetsmängd tillsammans om det behövs", "stor"]] }
  ];
  var BY_ID = {}; AREAS.forEach(function (a) { BY_ID[a.id] = a; });
  var LEVEL = { enkel: "Enkelt att börja med", medel: "Kräver lite planering", stor: "Större förändring" };
  var MAX = 3;
  var D = window.nvDoc;
  var form = document.querySelector('[data-stepper="anpassningsplanen"]');
  if (!form) return;

  // render area options
  var areaBox = document.getElementById("areas");
  areaBox.innerHTML = '<legend class="visually-hidden">Det som tar energi</legend>' + AREAS.map(function (a) {
    return '<label class="option"><input type="checkbox" name="omraden" value="' + a.id + '"><span><span class="t">' + a.t +
      '</span><span class="d more">' + a.d + "</span></span></label>";
  }).join("");

  function picked(data) { return (data.omraden || []).filter(function (id) { return BY_ID[id]; }); }

  function limitAreas() {
    var boxes = areaBox.querySelectorAll("input");
    var n = Array.prototype.filter.call(boxes, function (b) { return b.checked; }).length;
    Array.prototype.forEach.call(boxes, function (b) { b.disabled = !b.checked && n >= MAX; });
    document.getElementById("area-count").textContent = n === MAX ? "Tre valda – avmarkera något om du vill byta." : n + " av " + MAX + " valda";
  }
  areaBox.addEventListener("change", limitAreas);

  function renderHelps(data) {
    var box = document.getElementById("helps");
    var prev = data.hjalper || [];
    var html = picked(data).map(function (id) {
      var a = BY_ID[id];
      return '<fieldset class="options" style="margin-top:22px"><legend style="font-weight:600;font-size:18px;margin-bottom:10px">' + a.t + "</legend>" +
        a.helps.map(function (h, i) {
          var v = id + ":" + i;
          return '<label class="option"><input type="checkbox" name="hjalper" value="' + v + '"' + (prev.indexOf(v) !== -1 ? " checked" : "") +
            '><span class="t">' + h + "</span></label>";
        }).join("") + "</fieldset>";
    }).join("");
    box.innerHTML = html || '<p class="explain">Välj minst ett område i föregående steg.</p>';
  }

  function renderSuggestions(data) {
    var box = document.getElementById("suggestions");
    var prev = data.forslag;
    var html = picked(data).map(function (id) {
      var a = BY_ID[id];
      return '<fieldset class="options" style="margin-top:22px"><legend style="font-weight:600;font-size:18px;margin-bottom:10px">' + a.t + "</legend>" +
        a.sugg.map(function (s, i) {
          var v = id + ":" + i;
          var on = prev ? prev.indexOf(v) !== -1 : i < 2 && s[1] === "enkel";
          return '<label class="option"><input type="checkbox" name="forslag" value="' + v + '"' + (on ? " checked" : "") +
            '><span><span class="t">' + s[0] + '</span><span class="d">' + LEVEL[s[1]] + "</span></span></label>";
        }).join("") + "</fieldset>";
    }).join("");
    box.innerHTML = html || '<p class="explain">Välj minst ett område i steg 2.</p>';
  }

  function chosenSuggestions(data) {
    return (data.forslag || []).map(function (v) {
      var p = v.split(":"); var a = BY_ID[p[0]]; return a && a.sugg[+p[1]] ? { area: a, s: a.sugg[+p[1]] } : null;
    }).filter(Boolean);
  }

  function renderDoc(data) {
    var follow = data.uppfoljning || D.addDays(D.today(), 28);
    var fu = document.getElementById("uppfoljning");
    if (fu && !fu.value) fu.value = follow;
    var who = data.roll === "medarbetare" ? "Jag" : "Medarbetaren";
    var areas = picked(data).map(function (id) { return BY_ID[id]; });
    var helps = (data.hjalper || []).map(function (v) { var p = v.split(":"); var a = BY_ID[p[0]]; return a ? a.helps[+p[1]] : null; }).filter(Boolean);
    var sugg = chosenSuggestions(data);
    var html = "<h2>Underlag inför samtal om arbetsanpassning</h2>" +
      '<p class="doc-meta">Upprättat ' + D.fmt(D.today()) + " · Följs upp " + D.fmt(follow) + "</p>" +
      "<h3>Det här tar energi i arbetet</h3><ul>" + areas.map(function (a) { return "<li><strong>" + a.t + ".</strong> " + a.doc + "</li>"; }).join("") + "</ul>" +
      (helps.length ? "<h3>Det här har hjälpt</h3><ul>" + helps.map(function (h) { return "<li>" + D.esc(h) + "</li>"; }).join("") + "</ul>" : "") +
      (data.egen ? "<h3>Med egna ord</h3><p>" + D.esc(data.egen).replace(/\n/g, "<br>") + "</p>" : "") +
      "<h3>Förslag att prova</h3>" +
      (sugg.length ? "<table><thead><tr><th scope='col'>Förslag</th><th scope='col'>Område</th><th scope='col'>Beslut</th></tr></thead><tbody>" +
        sugg.map(function (x) { return "<tr><td>" + x.s[0] + "</td><td>" + x.area.t + "</td><td>Ja · Nej · Prova</td></tr>"; }).join("") + "</tbody></table>"
        : "<p>Inga förslag valda ännu.</p>") +
      "<h3>Uppföljning</h3><p>" + who + " och chefen går igenom hur anpassningarna fungerar den " + D.fmt(follow) +
      ". Det som inte fungerar ändras eller ersätts.</p>" +
      "<h3>Bakgrund</h3><p>Arbetsgivaren ska utreda behovet av anpassning, vidta de åtgärder som behövs och följa upp dem (Arbetsmiljöverkets föreskrifter AFS 2023:2, kapitel 3). Underlaget beskriver hur arbetet fungerar – det förutsätter ingen diagnos.</p>" +
      '<div class="sign"><div>Medarbetare</div><div>Chef</div></div>';
    document.getElementById("doc").innerHTML = html;
  }

  function renderLive(data) {
    var areas = picked(data).map(function (id) { return BY_ID[id].t; });
    var n = (data.forslag || []).length;
    document.getElementById("live").innerHTML =
      "<p style='margin:0;font-weight:600'>Det här tar energi</p>" +
      (areas.length ? "<ul style='margin:6px 0 0;padding-left:18px'>" + areas.map(function (t) { return "<li>" + t + "</li>"; }).join("") + "</ul>"
        : "<p style='margin:6px 0 0;color:var(--muted)'>Inget valt ännu.</p>") +
      (n ? "<p style='margin:12px 0 0'><strong>" + n + "</strong> förslag valda</p>" : "");
  }

  // Steps 3–4 build their inputs from earlier answers. Rebuild them from the saved state
  // BEFORE the stepper restores it, or a reload on the last step would find nothing to tick.
  var saved = null;
  try { saved = JSON.parse(localStorage.getItem("nv_tool_anpassningsplanen") || "null"); } catch (e) { saved = null; }
  if (saved && saved.data) { renderHelps(saved.data); renderSuggestions(saved.data); }

  var stepper = window.nvStepper(form, {
    validate: function (step, data) {
      if (step === 1 && picked(data).length === 0) return "Välj minst ett område för att gå vidare.";
      if (step === 3 && !(data.forslag || []).length) return "Välj minst ett förslag – du kan ändra dig i samtalet.";
      return null;
    },
    onStep: function (step, data) {
      limitAreas();
      if (step === 2) renderHelps(data);
      if (step === 3) renderSuggestions(data);
      if (step === 4) { renderDoc(data); if (window.nv) window.nv.usage("anpassningsplanen", { done: true, areas: picked(data) }); }
      renderLive(data);
    },
    onChange: function (step, data) { renderLive(data); if (step === 4) renderDoc(data); }
  });
  document.getElementById("copy-doc").addEventListener("click", function (e) { D.copyText(document.getElementById("doc"), e.target); });
  renderLive(stepper.data());
})();
