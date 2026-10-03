/* Neurovibe stepper — one question per screen.
   Markup: <form data-stepper="key"> containing <section data-step="n" data-label="…"> blocks,
   an <ol class="steps-rail" data-rail>, a <div class="progress-bar" data-bar> and buttons
   [data-next] / [data-prev]. Answers are kept in localStorage under nv_tool_<key> so a visitor
   can leave and come back; "Börja om" clears them. Each tool hooks in via
   window.nvStepper(form, { onStep(n, data), validate(n, data) → message|null }). */
(function () {
  "use strict";

  function serialize(form) {
    var data = {};
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || el.disabled) return;
      if (el.type === "checkbox") {
        if (!data[el.name]) data[el.name] = [];
        if (el.checked) data[el.name].push(el.value);
      } else if (el.type === "radio") {
        if (el.checked) data[el.name] = el.value;
        else if (!(el.name in data)) data[el.name] = "";
      } else {
        data[el.name] = el.value;
      }
    });
    return data;
  }

  function restore(form, data) {
    Array.prototype.forEach.call(form.elements, function (el) {
      if (!el.name || !(el.name in data)) return;
      var v = data[el.name];
      if (el.type === "checkbox") el.checked = Array.isArray(v) && v.indexOf(el.value) !== -1;
      else if (el.type === "radio") el.checked = v === el.value;
      else el.value = v;
    });
  }

  window.nvStepper = function (form, hooks) {
    hooks = hooks || {};
    var key = "nv_tool_" + form.dataset.stepper;
    var steps = Array.prototype.slice.call(form.querySelectorAll("[data-step]"));
    var rail = document.querySelector("[data-rail]");
    var bar = document.querySelector("[data-bar]");
    var counter = document.querySelectorAll("[data-step-count]");
    var current = 0;

    var saved = null;
    try { saved = JSON.parse(localStorage.getItem(key) || "null"); } catch (e) { saved = null; }
    var params = new URLSearchParams(window.location.search);
    if (saved && saved.data) restore(form, saved.data);
    if (params.get("roll") && form.elements.roll) {
      Array.prototype.forEach.call(form.querySelectorAll('[name="roll"]'), function (r) { r.checked = r.value === params.get("roll"); });
    }

    function save() {
      try { localStorage.setItem(key, JSON.stringify({ step: current, data: serialize(form), at: Date.now() })); } catch (e) { /* ok */ }
    }

    function paintRail() {
      if (rail) {
        Array.prototype.forEach.call(rail.children, function (li, i) {
          li.className = i < current ? "done" : (i === current ? "current" : "");
          if (i === current) li.setAttribute("aria-current", "step"); else li.removeAttribute("aria-current");
          var dot = li.querySelector(".dot");
          if (dot) dot.innerHTML = i < current
            ? '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" aria-hidden="true"><path d="M5 12l4 4 10-10"/></svg>'
            : String(i + 1);
          var btn = li.querySelector("button");
          if (btn) btn.disabled = i > current;
        });
      }
      if (bar) {
        Array.prototype.forEach.call(bar.children, function (s, i) {
          s.className = i < current ? "done" : (i === current ? "current" : "");
        });
      }
      Array.prototype.forEach.call(counter, function (c) { c.textContent = "Steg " + (current + 1) + " av " + steps.length; });
    }

    function show(n, focus) {
      current = Math.max(0, Math.min(steps.length - 1, n));
      steps.forEach(function (s, i) { s.hidden = i !== current; });
      paintRail();
      var data = serialize(form);
      if (hooks.onStep) hooks.onStep(current, data);
      save();
      if (focus) {
        var h = steps[current].querySelector("h2");
        if (h) { h.setAttribute("tabindex", "-1"); h.focus({ preventScroll: true }); }
        var top = form.getBoundingClientRect().top + window.scrollY - 24;
        if (window.scrollY > top) window.scrollTo(0, top);
      }
      if (window.nv) window.nv.track("tool_step", { tool: form.dataset.stepper, step: current + 1 });
    }

    form.addEventListener("click", function (e) {
      var next = e.target.closest("[data-next]");
      var prev = e.target.closest("[data-prev]");
      var reset = e.target.closest("[data-reset]");
      if (next) {
        e.preventDefault();
        var data = serialize(form);
        var msg = hooks.validate ? hooks.validate(current, data) : null;
        var box = steps[current].querySelector("[data-error]");
        if (msg) { if (box) { box.textContent = msg; box.hidden = false; } return; }
        if (box) box.hidden = true;
        if (current === 0 && window.nv) window.nv.usage(form.dataset.stepper, { started: true });
        show(current + 1, true);
      }
      if (prev) { e.preventDefault(); show(current - 1, true); }
      if (reset) {
        e.preventDefault();
        try { localStorage.removeItem(key); } catch (er) { /* ok */ }
        form.reset();
        show(0, true);
      }
    });
    form.addEventListener("change", function () { save(); if (hooks.onChange) hooks.onChange(current, serialize(form)); });
    if (rail) {
      rail.addEventListener("click", function (e) {
        var b = e.target.closest("button[data-goto]");
        if (b && !b.disabled) show(+b.dataset.goto, true);
      });
    }
    form.addEventListener("submit", function (e) { e.preventDefault(); });

    show(saved && typeof saved.step === "number" ? saved.step : 0, false);
    return { show: show, data: function () { return serialize(form); }, current: function () { return current; } };
  };

  /* shared output helpers */
  window.nvDoc = {
    esc: function (s) { return String(s || "").replace(/[&<>"']/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]; }); },
    today: function () { return new Date().toISOString().slice(0, 10); },
    addDays: function (iso, n) { var d = new Date(iso + "T12:00:00"); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); },
    fmt: function (iso) {
      if (!iso) return "";
      var d = new Date(iso + "T12:00:00");
      return d.toLocaleDateString("sv-SE", { day: "numeric", month: "long", year: "numeric" });
    },
    copyText: function (el, btn) {
      var text = el.innerText;
      var done = function () { if (btn) { var o = btn.textContent; btn.textContent = "Kopierat"; setTimeout(function () { btn.textContent = o; }, 2000); } };
      if (navigator.clipboard) navigator.clipboard.writeText(text).then(done, function () {});
      else { var t = document.createElement("textarea"); t.value = text; document.body.appendChild(t); t.select(); document.execCommand("copy"); t.remove(); done(); }
    }
  };
})();
