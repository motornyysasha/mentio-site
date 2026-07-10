(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* ---------- reveal on scroll ---------- */
  if (!reduced && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".card, .step, details, .lead, section h2, .kicker");
    var groups = {};
    targets.forEach(function (el) {
      el.classList.add("reveal");
      var key = el.parentElement ? Array.prototype.indexOf.call(document.querySelectorAll("section, header"), el.closest("section, header")) : 0;
      groups[key] = groups[key] || [];
      groups[key].push(el);
      el.style.transitionDelay = Math.min(groups[key].length - 1, 5) * 70 + "ms";
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          e.target.addEventListener("transitionend", function h() {
            e.target.classList.remove("reveal", "in");
            e.target.style.transitionDelay = "";
            e.target.removeEventListener("transitionend", h);
          });
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---------- card tilt ---------- */
  if (!reduced && finePointer) {
    document.querySelectorAll(".card").forEach(function (c) {
      c.addEventListener("mousemove", function (e) {
        var r = c.getBoundingClientRect();
        var rx = ((e.clientY - r.top) / r.height - 0.5) * -4;
        var ry = ((e.clientX - r.left) / r.width - 0.5) * 4;
        c.style.transform = "perspective(700px) rotateX(" + rx.toFixed(2) + "deg) rotateY(" + ry.toFixed(2) + "deg) translateY(-2px)";
      });
      c.addEventListener("mouseleave", function () { c.style.transform = ""; });
    });
  }

  /* ---------- hero mouse glow ---------- */
  var hero = document.querySelector("header.hero");
  if (hero && !reduced && finePointer) {
    hero.addEventListener("mousemove", function (e) {
      var r = hero.getBoundingClientRect();
      hero.style.setProperty("--mx", ((e.clientX - r.left) / r.width * 100).toFixed(1) + "%");
      hero.style.setProperty("--my", ((e.clientY - r.top) / r.height * 100).toFixed(1) + "%");
    });
  }

  /* ---------- live AI demo ---------- */
  var demo = document.querySelector(".demo");
  if (demo && !reduced) {
    var q = demo.querySelector('[data-part="q"]');
    var ai = demo.querySelector('[data-part="a"]');
    var at = demo.querySelector('[data-part="atext"]');
    var recs = Array.prototype.slice.call(demo.querySelectorAll(".rec"));
    var qText = q.textContent, aText = at.textContent;
    var cycles = 0;

    function typeInto(el, text, speed) {
      el.textContent = "";
      var caret = document.createElement("span");
      caret.className = "caret";
      el.appendChild(caret);
      var i = 0;
      return new Promise(function (res) {
        (function tick() {
          if (i < text.length) {
            caret.before(document.createTextNode(text[i++]));
            setTimeout(tick, speed + Math.random() * 24);
          } else { caret.remove(); res(); }
        })();
      });
    }

    function resetState() {
      ai.style.opacity = "0";
      recs.forEach(function (r) { r.style.opacity = "0"; r.style.transform = "translateY(8px)"; });
      at.textContent = "";
      q.textContent = "";
    }

    function playOnce() {
      return sleep(700)
        .then(function () { return typeInto(q, qText, 26); })
        .then(function () { return sleep(550); })
        .then(function () { ai.style.opacity = "1"; return typeInto(at, aText, 13); })
        .then(function () {
          return recs.reduce(function (p, r) {
            return p.then(function () {
              return sleep(380).then(function () { r.style.opacity = "1"; r.style.transform = "none"; });
            });
          }, Promise.resolve());
        });
    }

    function loop() {
      resetState();
      playOnce().then(function () {
        cycles++;
        if (cycles < 3) { sleep(7000).then(loop); }
      });
    }

    var started = false;
    var dio = new IntersectionObserver(function (entries) {
      if (entries[0].isIntersecting && !started) { started = true; loop(); dio.disconnect(); }
    }, { threshold: 0.35 });
    dio.observe(demo);
  }

  /* ---------- lead delivery ---------- */
  var LEAD_ENDPOINT = window.LEAD_ENDPOINT || "";
  try { LEAD_ENDPOINT = LEAD_ENDPOINT || localStorage.getItem("leadEndpoint") || ""; } catch (e) {}
  function submitLead(payload) {
    payload.lang = document.documentElement.lang || "";
    payload.page = location.pathname;
    return fetch(LEAD_ENDPOINT, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    }).then(function (r) { if (!r.ok) throw new Error("relay " + r.status); });
  }
  window.__mentioLead = { enabled: function () { return !!LEAD_ENDPOINT; }, submit: submitLead };

  /* ---------- site scanner ---------- */
  document.querySelectorAll("form.scan-form").forEach(function (f) {
    var cfg;
    try { cfg = JSON.parse(f.getAttribute("data-cfg")); } catch (e) { return; }
    var input = f.querySelector("input");
    var btn = f.querySelector("button");
    var status = f.parentElement.querySelector(".scan-status");
    var DRE = /^[a-z0-9\u0400-\u04ff.-]+\.[a-z\u0400-\u04ff]{2,}$/i;
    var stage = 1, savedDomain = "";
    function domainOf() {
      return input.value.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
    }
    function reject(msg) {
      status.classList.remove("ok");
      status.textContent = msg;
      f.classList.add("invalid");
      input.focus();
    }
    input.addEventListener("input", function () { f.classList.remove("invalid"); });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (stage === 2) {
        var contact = input.value.trim();
        if (contact.length < 4) { reject(cfg.contactPh); return; }
        btn.disabled = true;
        submitLead({ type: "scan", domain: savedDomain, contact: contact }).then(function () {
          status.classList.add("ok");
          status.textContent = cfg.sent;
          f.hidden = true;
        }).catch(function () {
          status.classList.remove("ok");
          status.textContent = cfg.err;
          btn.disabled = false;
        });
        return;
      }
      var d = domainOf();
      if (!DRE.test(d)) { reject(cfg.invalid); return; }
      btn.disabled = true;
      status.classList.remove("ok");
      var chain = Promise.resolve();
      cfg.steps.forEach(function (s) {
        chain = chain.then(function () { status.textContent = s; return sleep(reduced ? 50 : 950); });
      });
      chain.then(function () {
        status.classList.add("ok");
        btn.disabled = false;
        if (LEAD_ENDPOINT) {
          savedDomain = d;
          stage = 2;
          status.textContent = cfg.doneForm;
          input.value = "";
          input.placeholder = cfg.contactPh;
          btn.textContent = cfg.send;
          input.focus();
        } else {
          status.textContent = cfg.done;
          window.location.href = "mailto:team@mentio.agency?subject=" +
            encodeURIComponent(cfg.subject + " " + d) + "&body=" +
            encodeURIComponent(cfg.body + " " + d);
        }
      });
    });
  });
})();

/* ---------- AI visibility quiz ---------- */
(function () {
  "use strict";
  document.querySelectorAll(".quiz").forEach(function (qz) {
    var cfg;
    try { cfg = JSON.parse(qz.getAttribute("data-cfg")); } catch (e) { return; }
    var qEl = qz.querySelector(".quiz-q");
    var countEl = qz.querySelector(".quiz-count");
    var bar = qz.querySelector(".quiz-progress span");
    var opts = qz.querySelector(".quiz-opts");
    var result = qz.querySelector(".quiz-result");
    var ring = qz.querySelector(".score-ring");
    var num = qz.querySelector(".score-num");
    var verdict = qz.querySelector(".quiz-verdict");
    var cta = qz.querySelector(".quiz-cta");
    var i = 0, sum = 0, n = cfg.qs.length, lastScore = 0;
    var site = document.createElement("input");
    site.className = "quiz-site"; site.type = "text"; site.autocomplete = "off";
    var scanIn = document.querySelector(".scan-form input");
    site.placeholder = scanIn ? scanIn.placeholder : "yoursite.com";
    result.insertBefore(site, cta);
    var hint = document.createElement("p");
    hint.className = "quiz-hint";
    try { hint.textContent = JSON.parse(document.querySelector(".scan-form").getAttribute("data-cfg")).invalid; }
    catch (e) { hint.textContent = "example.com"; }
    hint.hidden = true;
    result.insertBefore(hint, cta);
    function getDomain() {
      return site.value.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
    }
    function isValid(d) { return /^[a-z0-9\u0400-\u04ff.-]+\.[a-z\u0400-\u04ff]{2,}$/i.test(d); }
    var scanCfg = {};
    try { scanCfg = JSON.parse(document.querySelector(".scan-form").getAttribute("data-cfg")); } catch (e) {}
    var contact = null;
    if (window.__mentioLead && window.__mentioLead.enabled()) {
      contact = document.createElement("input");
      contact.className = "quiz-site"; contact.type = "text"; contact.autocomplete = "off";
      contact.placeholder = scanCfg.contactPh || "email";
      result.insertBefore(contact, hint);
      contact.addEventListener("input", function () { contact.classList.remove("invalid"); buildHref(); });
    }
    function isReady() {
      var ok = isValid(getDomain());
      if (contact) ok = ok && contact.value.trim().length >= 4;
      return ok;
    }
    function buildHref() {
      var ready = isReady();
      cta.classList.toggle("disabled", !ready);
      if (isValid(getDomain())) { site.classList.remove("invalid"); hint.hidden = true; }
      if (ready && !contact) {
        cta.href = "mailto:team@mentio.agency?subject=" +
          encodeURIComponent(cfg.subj.replace("{s}", lastScore) + " \u2014 " + getDomain()) + "&body=" +
          encodeURIComponent(cfg.body.replace("{s}", lastScore) + getDomain());
      }
    }
    site.addEventListener("input", buildHref);
    cta.addEventListener("click", function (e) {
      if (!isValid(getDomain())) {
        e.preventDefault();
        site.classList.add("invalid");
        hint.hidden = false;
        site.focus();
        return;
      }
      if (!contact) return;
      e.preventDefault();
      if (contact.value.trim().length < 4) { contact.classList.add("invalid"); contact.focus(); return; }
      if (cta.classList.contains("sending")) return;
      cta.classList.add("sending");
      window.__mentioLead.submit({ type: "quiz", score: lastScore, domain: getDomain(), contact: contact.value.trim() })
        .then(function () {
          site.hidden = true; contact.hidden = true; cta.hidden = true;
          hint.hidden = false;
          hint.classList.add("ok");
          hint.textContent = scanCfg.sent || "OK";
        })
        .catch(function () {
          cta.classList.remove("sending");
          hint.hidden = false;
          hint.textContent = scanCfg.err || "Error";
        });
    });

    function show() {
      countEl.textContent = (i + 1) + " / " + n;
      qEl.textContent = cfg.qs[i];
      bar.style.width = (i / n * 100) + "%";
    }
    function finish() {
      var score = Math.round(sum / (2 * n) * 100);
      bar.style.width = "100%";
      qEl.hidden = true; opts.hidden = true; countEl.hidden = true;
      result.hidden = false;
      var tier = score < 40 ? "low" : score < 75 ? "mid" : "high";
      verdict.textContent = cfg.tiers[tier];
      ring.style.background = "conic-gradient(#F0512F " + score + "%, #2A2A36 0)";
      var cur = 0;
      var t = setInterval(function () {
        cur += Math.max(1, Math.round(score / 30));
        if (cur >= score) { cur = score; clearInterval(t); }
        num.innerHTML = cur + "<small>/100</small>";
      }, 30);
      lastScore = score;
      buildHref();
    }
    opts.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b || i >= n) return;
      sum += Number(b.getAttribute("data-v"));
      i++;
      if (i < n) show(); else finish();
    });
    qz.querySelector(".quiz-restart").addEventListener("click", function () {
      i = 0; sum = 0;
      qEl.hidden = false; opts.hidden = false; countEl.hidden = false;
      result.hidden = true;
      show();
    });
    show();
  });

  /* ---------- loss calculator ---------- */
  document.querySelectorAll(".calc").forEach(function (c) {
    var cfg;
    try { cfg = JSON.parse(c.getAttribute("data-cfg")); } catch (e) { return; }
    var clients = c.querySelector('[data-in="clients"]');
    var check = c.querySelector('[data-in="check"]');
    var AI_SHARE = 0.25;
    var money = new Intl.NumberFormat(cfg.locale, { style: "currency", currency: cfg.currency, maximumFractionDigits: 0 });
    var ints = new Intl.NumberFormat(cfg.locale, { maximumFractionDigits: 0 });
    function upd() {
      var cl = +clients.value, ch = +check.value;
      c.querySelector('[data-val="clients"]').textContent = ints.format(cl);
      c.querySelector('[data-val="check"]').textContent = money.format(ch);
      var missed = cl * AI_SHARE / (1 - AI_SHARE);
      var perMonth = missed * ch;
      c.querySelector(".calc-big").textContent = "≈ " + money.format(perMonth) + " " + cfg.mo;
      c.querySelector(".calc-sub").textContent = money.format(perMonth * 12) + " " + cfg.yr + " · " + cfg.cust.replace("{n}", ints.format(Math.round(missed)));
    }
    [clients, check].forEach(function (inp) { inp.addEventListener("input", upd); });
    upd();
  });
})();
