/* Volleyball Liga Klasse 8: Filter, Einblenden, Notenrechner, Ligatabelle. Kein Framework, keine externen Aufrufe. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  /* Einblenden beim Scrollen (nur wenn Bewegung erlaubt ist) */
  var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var revealEls = document.querySelectorAll(".reveal");
  if (reduce || !("IntersectionObserver" in window)) {
    revealEls.forEach(function (el) { el.classList.add("in"); });
  } else {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) { e.target.classList.add("in"); io.unobserve(e.target); }
      });
    }, { threshold: 0.15 });
    revealEls.forEach(function (el, i) {
      el.style.setProperty("--d", (i % 4) * 60 + "ms");
      io.observe(el);
    });
  }

  /* Spielkarten nach Stunde filtern */
  var chips = document.querySelectorAll(".chip[data-filter]");
  var games = document.querySelectorAll("#game-list .game");
  chips.forEach(function (chip) {
    chip.addEventListener("click", function () {
      chips.forEach(function (c) { c.setAttribute("aria-pressed", c === chip ? "true" : "false"); });
      var f = chip.getAttribute("data-filter");
      games.forEach(function (g) { g.hidden = !(f === "alle" || g.getAttribute("data-stunde") === f); });
    });
  });

  /* Notenrechner: Technik (Pritschen + Baggern, 20 Punkte) und Spiel (12 Punkte) */
  var form = document.getElementById("rechner");
  if (form) {
    var MAX = { pritschen: 10, baggern: 10, spiel: 12 };
    /* Schluessel aus Fabis Standard: ab 90/80/60/40/20 Prozent gleich Note 1 bis 5 */
    function noteFor(points, max) {
      var p = Math.round(points / max * 1e6) / 1e6;
      if (p >= 0.9) return 1;
      if (p >= 0.8) return 2;
      if (p >= 0.6) return 3;
      if (p >= 0.4) return 4;
      if (p >= 0.2) return 5;
      return 6;
    }
    function read(k) {
      var input = form.elements[k];
      var err = document.getElementById("e-" + k);
      var raw = input.value.trim();
      err.textContent = "";
      input.removeAttribute("aria-invalid");
      if (raw === "") return null;
      var v = Number(raw.replace(",", "."));
      if (isNaN(v) || v < 0 || v > MAX[k]) {
        err.textContent = "Bitte 0 bis " + MAX[k] + " eingeben.";
        input.setAttribute("aria-invalid", "true");
        return null;
      }
      return v;
    }
    function show(id, note, info) {
      document.getElementById("r-" + id).textContent = note;
      document.getElementById("p-" + id).textContent = info;
    }
    function update() {
      var pr = read("pritschen"), ba = read("baggern"), sp = read("spiel");
      if (pr !== null && ba !== null) {
        show("technik", String(noteFor(pr + ba, 20)), (pr + ba) + " von 20 Punkten");
      } else {
        show("technik", "-", "");
      }
      if (sp !== null) {
        show("spiel", String(noteFor(sp, 12)), sp + " von 12 Punkten");
      } else {
        show("spiel", "-", "");
      }
    }
    form.addEventListener("input", update);
    form.addEventListener("submit", function (e) { e.preventDefault(); });
    update();
  }

  /* Ligatabelle: Eingaben bleiben im Browser (localStorage), Summe und Rang rechnet die Seite */
  var liga = document.querySelector("table.liga");
  if (liga) {
    var KEY = "volleyball8-liga";
    var inputs = liga.querySelectorAll("input");
    var state = {};
    try { state = JSON.parse(localStorage.getItem(KEY) || "{}") || {}; } catch (e) { state = {}; }

    function keyOf(el) {
      return el.hasAttribute("data-name") ? "n" + el.getAttribute("data-name")
        : "p" + el.getAttribute("data-team") + "-" + el.getAttribute("data-col");
    }
    function save() {
      try { localStorage.setItem(KEY, JSON.stringify(state)); } catch (e) { /* Speichern nicht moeglich, Tabelle funktioniert trotzdem */ }
    }
    function num(el) {
      var v = Number(String(el.value).replace(",", "."));
      return isNaN(v) || el.value.trim() === "" ? 0 : v;
    }
    function recalc() {
      var sums = [];
      for (var t = 0; t < 4; t++) {
        var s = 0;
        liga.querySelectorAll('input.pt[data-team="' + t + '"]').forEach(function (el) { s += num(el); });
        sums.push(s);
        liga.querySelector('[data-sum="' + t + '"]').textContent = String(Math.round(s * 100) / 100);
      }
      var any = sums.some(function (s) { return s > 0; });
      for (var i = 0; i < 4; i++) {
        var rank = 1;
        for (var j = 0; j < 4; j++) { if (sums[j] > sums[i]) rank++; }
        liga.querySelector('[data-rank="' + i + '"]').textContent = any ? String(rank) : "-";
        liga.querySelector('tr[data-team="' + i + '"]').classList.toggle("first", any && rank === 1);
      }
    }
    inputs.forEach(function (el) {
      var k = keyOf(el);
      if (state[k] !== undefined) el.value = state[k];
      el.addEventListener("input", function () { state[k] = el.value; save(); recalc(); });
    });
    recalc();

    /* Leeren mit zweitem Klick statt Dialog (Dialoge sind auf dem iPad unzuverlaessig) */
    var reset = document.getElementById("liga-reset");
    if (reset) {
      var armed = false, timer = null;
      reset.addEventListener("click", function () {
        if (!armed) {
          armed = true;
          reset.textContent = "Wirklich leeren? Nochmal klicken";
          timer = setTimeout(function () { armed = false; reset.textContent = "Tabelle leeren"; }, 4000);
          return;
        }
        clearTimeout(timer);
        armed = false;
        reset.textContent = "Tabelle leeren";
        state = {};
        try { localStorage.removeItem(KEY); } catch (e) { /* nichts zu tun */ }
        inputs.forEach(function (el) { el.value = el.hasAttribute("data-name") ? el.defaultValue : ""; });
        recalc();
      });
    }
  }

  /* Spielkarten: auf dem Handy eingeklappt, per Link oder Tippen auf */
  var cards = document.querySelectorAll("details.game");
  if (cards.length && window.matchMedia("(max-width: 860px)").matches) {
    cards.forEach(function (d) { d.open = false; });
  }
  function openTarget() {
    var h = location.hash;
    if (h.length > 1) {
      var el = document.getElementById(decodeURIComponent(h.slice(1)));
      if (el && el.tagName === "DETAILS") { el.open = true; el.scrollIntoView({ block: "start" }); }
    }
  }
  window.addEventListener("hashchange", openTarget);
  openTarget();
  window.addEventListener("beforeprint", function () { cards.forEach(function (d) { d.open = true; }); });

  /* Aktuellen Menuepunkt ins Sichtfeld holen (Handy) */
  var cur = document.querySelector(".nav a[aria-current]");
  if (cur && cur.scrollIntoView) { cur.scrollIntoView({ inline: "center", block: "nearest" }); }

  /* Timer: Countdown mit Signalton, Vibration und Bildschirm-an */
  var timer = document.getElementById("timer");
  if (timer) {
    var clock = document.getElementById("clock"), startBtn = document.getElementById("t-start"),
        resetBtn = document.getElementById("t-reset"), info = document.getElementById("t-info");
    var total = 6 * 60, left = total, tick = null, endAt = 0, wake = null, ctx = null;
    function fmt(sec) {
      var m = Math.floor(sec / 60), s = sec % 60;
      return (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }
    function draw() { clock.textContent = fmt(Math.max(0, Math.ceil(left))); }
    function beep(times) {
      try {
        ctx = ctx || new (window.AudioContext || window.webkitAudioContext)();
        for (var i = 0; i < times; i++) {
          var o = ctx.createOscillator(), g = ctx.createGain();
          o.frequency.value = 880; o.connect(g); g.connect(ctx.destination);
          var t0 = ctx.currentTime + i * 0.45;
          g.gain.setValueAtTime(0.35, t0); g.gain.exponentialRampToValueAtTime(0.001, t0 + 0.35);
          o.start(t0); o.stop(t0 + 0.38);
        }
      } catch (e) { /* kein Ton moeglich, die Anzeige blinkt trotzdem */ }
      try { if (navigator.vibrate) navigator.vibrate([300, 150, 300, 150, 300]); } catch (e) { /* nicht unterstuetzt */ }
    }
    function keepAwake(on) {
      try {
        if (on && navigator.wakeLock) { navigator.wakeLock.request("screen").then(function (w) { wake = w; }, function () {}); }
        else if (wake) { wake.release(); wake = null; }
      } catch (e) { /* Bildschirm-an nicht verfuegbar */ }
    }
    function stop() { clearInterval(tick); tick = null; startBtn.textContent = "Start"; clock.classList.remove("run"); keepAwake(false); }
    function loop() {
      left = (endAt - Date.now()) / 1000;
      if (left <= 0) { left = 0; draw(); stop(); clock.classList.add("done"); info.textContent = "Zeit ist um. Wechsel!"; beep(3); return; }
      draw();
    }
    startBtn.addEventListener("click", function () {
      if (tick) { left = (endAt - Date.now()) / 1000; stop(); startBtn.textContent = "Weiter"; return; }
      if (left <= 0) { left = total; }
      clock.classList.remove("done");
      endAt = Date.now() + left * 1000;
      tick = setInterval(loop, 250);
      startBtn.textContent = "Pause"; clock.classList.add("run"); info.textContent = "Läuft.";
      keepAwake(true);
      try { ctx = ctx || new (window.AudioContext || window.webkitAudioContext)(); if (ctx.resume) ctx.resume(); } catch (e) { /* kein Ton */ }
      loop();
    });
    resetBtn.addEventListener("click", function () { stop(); clock.classList.remove("done"); left = total; draw(); startBtn.textContent = "Start"; info.textContent = "Zeit wählen und Start drücken."; });
    timer.querySelectorAll(".chip[data-min]").forEach(function (b) {
      b.addEventListener("click", function () {
        stop(); clock.classList.remove("done");
        total = Number(b.getAttribute("data-min")) * 60; left = total; draw(); startBtn.textContent = "Start";
        timer.querySelectorAll(".chip").forEach(function (c) { c.setAttribute("aria-pressed", c === b ? "true" : "false"); });
      });
    });
    document.addEventListener("visibilitychange", function () { if (tick && document.visibilityState === "visible") keepAwake(true); });
    draw();
  }
})();
