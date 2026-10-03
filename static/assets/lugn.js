/* Neurovibe — shared page behaviour: reading settings and analytics consent.
   Consent Mode v2: Google tags are loaded with everything denied (set inline in <head>),
   and only flipped to granted when the visitor says yes here. */
(function () {
  "use strict";

  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) { /* private mode */ } }
  };

  /* ---------- reading settings ---------- */
  var SETTINGS = ["rs-large", "rs-calm", "rs-short"];
  function applySettings() {
    SETTINGS.forEach(function (cls) {
      document.body.classList.toggle(cls, store.get("nv_" + cls) === "1");
    });
  }

  function bindSettings() {
    var toggle = document.getElementById("settings-toggle");
    var panel = document.getElementById("settings-panel");
    if (!toggle || !panel) return;
    toggle.addEventListener("click", function () {
      var open = panel.hasAttribute("hidden");
      if (open) panel.removeAttribute("hidden"); else panel.setAttribute("hidden", "");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && !panel.hasAttribute("hidden")) {
        panel.setAttribute("hidden", "");
        toggle.setAttribute("aria-expanded", "false");
        toggle.focus();
      }
    });
    SETTINGS.forEach(function (cls) {
      var box = document.getElementById("set-" + cls);
      if (!box) return;
      box.checked = store.get("nv_" + cls) === "1";
      box.addEventListener("change", function () {
        store.set("nv_" + cls, box.checked ? "1" : "0");
        applySettings();
      });
    });
  }

  /* ---------- consent ---------- */
  var CONSENT_KEY = "nv_consent_v2";
  function grant() {
    if (typeof window.gtag === "function") {
      window.gtag("consent", "update", { analytics_storage: "granted" });
    }
  }
  function bindConsent() {
    var box = document.getElementById("consent");
    if (!box) return;
    var choice = store.get(CONSENT_KEY);
    if (choice === "yes") { grant(); return; }
    if (choice === "no") return;
    box.removeAttribute("hidden");
    box.querySelector("[data-consent=yes]").addEventListener("click", function () {
      store.set(CONSENT_KEY, "yes"); grant(); box.setAttribute("hidden", "");
    });
    box.querySelector("[data-consent=no]").addEventListener("click", function () {
      store.set(CONSENT_KEY, "no"); box.setAttribute("hidden", "");
    });
  }
  window.nvReopenConsent = function () {
    store.set(CONSENT_KEY, "");
    var box = document.getElementById("consent");
    if (box) { box.removeAttribute("hidden"); }
  };

  /* ---------- tiny helpers shared by the tools ---------- */
  window.nv = {
    store: store,
    track: function (name, payload) {
      if (typeof window.gtag === "function") window.gtag("event", name, payload || {});
    },
    usage: function (tool, meta) {
      // anonymous usage count — no free text is ever sent
      try {
        fetch("/api/tool-usage", { method: "POST", headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ tool: tool, metadata: meta || {} }) });
      } catch (e) { /* offline */ }
    }
  };

  function init() { applySettings(); bindSettings(); bindConsent(); }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
