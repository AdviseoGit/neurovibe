/*
 * Neurovibe leadflow — ett gemensamt script för all lead-fångst.
 *
 * Ersätter de kopierade submitLeadMagnet()-varianterna på varje sida.
 * Lägg till på en sida:  <script src="/static/leadflow.js" defer></script>
 *
 * Använd sedan ett vanligt formulär:
 *
 *   <form data-nv-lead data-segment="arbetsgivare" data-offer="b2b-genomlysning">
 *     <input name="email" type="email" required>
 *     <input name="company">
 *     <select name="role">...</select>
 *     <input type="checkbox" name="consent" required>
 *     <button type="submit">Skicka</button>
 *   </form>
 *
 * Valfria attribut på formuläret:
 *   data-segment   individ | arbetsgivare | partner   (default: individ)
 *   data-offer     vilket erbjudande som konverterade  (default: data-segment)
 *   data-endpoint  överskriv API-vägen
 *   data-success   CSS-selector till en ruta som visas i stället för formuläret
 *   data-error     CSS-selector till en ruta för felmeddelanden
 *   data-redirect  URL att skicka vidare till, eller "auto" för /tack.html
 *                  (utan attributet visas bekräftelsen inline)
 */
(function () {
  "use strict";

  var ENDPOINTS = {
    individ: "/api/lead",
    arbetsgivare: "/api/b2b-lead",
    partner: "/api/partner-lead"
  };

  var UTM_KEYS = ["utm_source", "utm_medium", "utm_campaign"];
  var STORE_KEY = "nv_attribution";

  /* --- Attribution -----------------------------------------------------
   * Fångas en gång per session, inte per sida. Annars tappas kampanjkällan
   * så fort besökaren klickar sig vidare till en annan artikel innan hen
   * fyller i formuläret — vilket är precis vad de flesta gör.
   */
  function captureAttribution() {
    var stored = {};
    try {
      stored = JSON.parse(sessionStorage.getItem(STORE_KEY) || "{}");
    } catch (e) {
      stored = {};
    }

    var params = new URLSearchParams(window.location.search);
    var found = false;
    UTM_KEYS.forEach(function (key) {
      var value = params.get(key);
      if (value && !stored[key]) {
        stored[key] = value.slice(0, 120);
        found = true;
      }
    });

    if (!stored.referrer && document.referrer &&
        document.referrer.indexOf(window.location.host) === -1) {
      stored.referrer = document.referrer.slice(0, 200);
      found = true;
    }
    if (!stored.landing_page) {
      stored.landing_page = window.location.pathname;
      found = true;
    }

    if (found) {
      try {
        sessionStorage.setItem(STORE_KEY, JSON.stringify(stored));
      } catch (e) { /* privat läge — kör vidare utan attribution */ }
    }
    return stored;
  }

  var attribution = captureAttribution();

  /* --- Mätning --------------------------------------------------------- */
  function track(eventName, payload) {
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, payload);
    }
  }

  /* --- Fältinsamling --------------------------------------------------- */
  function collect(form) {
    var data = {};
    var elements = form.querySelectorAll("input, select, textarea");
    Array.prototype.forEach.call(elements, function (el) {
      if (!el.name || el.disabled) return;
      if (el.type === "checkbox") {
        data[el.name] = el.checked;
      } else if (el.type === "radio") {
        if (el.checked) data[el.name] = el.value;
      } else if (el.value) {
        data[el.name] = el.value.trim();
      }
    });
    return data;
  }

  function messageBox(form, selector, fallbackText, tone) {
    var box = selector ? document.querySelector(selector) : null;
    if (box) {
      box.classList.remove("hidden");
      return box;
    }
    // Ingen förberedd ruta på sidan — skapa en så att användaren aldrig
    // lämnas utan återkoppling.
    var created = document.createElement("p");
    created.className = "nv-flash mt-4 text-sm font-medium";
    created.style.color = tone === "error" ? "#FF6B6B" : "#4ADE80";
    created.textContent = fallbackText;
    form.parentNode.insertBefore(created, form.nextSibling);
    return created;
  }

  /* --- Inskick --------------------------------------------------------- */
  function submit(form, event) {
    event.preventDefault();

    var segment = form.dataset.segment || "individ";
    var offer = form.dataset.offer || segment;
    var endpoint = form.dataset.endpoint || ENDPOINTS[segment] || ENDPOINTS.individ;
    var button = form.querySelector('button[type="submit"], button:not([type])');
    var originalLabel = button ? button.innerHTML : "";

    var fields = collect(form);
    if (!fields.email) return;

    var consentInput = form.querySelector('input[name="consent"]');
    if (consentInput && !consentInput.checked) {
      messageBox(form, form.dataset.error,
        "Du behöver godkänna hur vi hanterar dina uppgifter för att fortsätta.", "error");
      return;
    }

    var payload = {
      email: fields.email,
      name: fields.name || null,
      role: fields.role || null,
      company: fields.company || null,
      company_size: fields.company_size || null,
      need: fields.need || null,
      timeline: fields.timeline || null,
      phone: fields.phone || null,
      message: fields.message || null,
      consent: !!fields.consent,
      segment: segment,
      offer: offer,
      source_page: window.location.pathname,
      referrer: attribution.referrer || null,
      utm_source: attribution.utm_source || null,
      utm_medium: attribution.utm_medium || null,
      utm_campaign: attribution.utm_campaign || null
    };

    if (button) {
      button.disabled = true;
      button.innerHTML = "Skickar...";
    }

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    })
      .then(function (res) {
        if (!res.ok) throw new Error("HTTP " + res.status);
        return res.json();
      })
      .then(function (result) {
        track("generate_lead", {
          segment: segment,
          offer: offer,
          page: window.location.pathname,
          campaign: attribution.utm_campaign || "(direkt)"
        });

        // Default är inline-bekräftelse: en läsare mitt i en guide ska inte
        // ryckas bort från texten. Sätt data-redirect på de formulär där en
        // riktig tacksida med nästa steg är hela poängen (B2B/partner).
        if (form.dataset.redirect) {
          var target = form.dataset.redirect === "auto"
            ? ((result && result.next) || "/tack.html?segment=" + segment)
            : form.dataset.redirect;
          window.location.href = target + "&offer=" + encodeURIComponent(offer);
          return;
        }
        form.style.display = "none";
        messageBox(form, form.dataset.success,
          "Tack! Vi har skickat en bekräftelse till " + payload.email + ".", "ok");
      })
      .catch(function (err) {
        console.error("[leadflow]", err);
        messageBox(form, form.dataset.error,
          "Något gick fel på vår sida. Mejla simon@adviseo.se och vi hör av oss direkt.",
          "error");
        if (button) {
          button.disabled = false;
          button.innerHTML = originalLabel;
        }
      });
  }

  /* --- Uppkoppling ----------------------------------------------------- */
  function bind() {
    var forms = document.querySelectorAll("form[data-nv-lead]");
    Array.prototype.forEach.call(forms, function (form) {
      if (form.dataset.nvBound === "true") return;
      form.dataset.nvBound = "true";
      form.addEventListener("submit", function (event) { submit(form, event); });

      // Ett engångs-event per formulär när besökaren börjar fylla i det.
      // Skillnaden mellan "sett formuläret" och "börjat fylla i" är den
      // enda siffra som säger om ett fält är för krångligt.
      var started = false;
      form.addEventListener("focusin", function () {
        if (started) return;
        started = true;
        track("lead_form_start", {
          segment: form.dataset.segment || "individ",
          offer: form.dataset.offer || "okänt",
          page: window.location.pathname
        });
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", bind);
  } else {
    bind();
  }

  // Exponera för dynamiskt inlagda formulär (t.ex. i chatt-flödet).
  window.nvLeadflow = { bind: bind, track: track, attribution: attribution };
})();
