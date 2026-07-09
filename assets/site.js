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

  /* ---------- site scanner ---------- */
  document.querySelectorAll("form.scan-form").forEach(function (f) {
    var cfg;
    try { cfg = JSON.parse(f.getAttribute("data-cfg")); } catch (e) { return; }
    var input = f.querySelector("input");
    var btn = f.querySelector("button");
    var status = f.parentElement.querySelector(".scan-status");
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      var d = input.value.trim().toLowerCase().replace(/^https?:\/\//, "").replace(/\/.*$/, "");
      if (!/^[a-z0-9Ѐ-ӿ.-]+\.[a-zЀ-ӿ]{2,}$/i.test(d)) {
        status.classList.remove("ok");
        status.textContent = cfg.invalid;
        return;
      }
      btn.disabled = true;
      status.classList.remove("ok");
      var chain = Promise.resolve();
      cfg.steps.forEach(function (s) {
        chain = chain.then(function () { status.textContent = s; return sleep(reduced ? 50 : 950); });
      });
      chain.then(function () {
        status.classList.add("ok");
        status.textContent = cfg.done;
        btn.disabled = false;
        window.location.href = "mailto:team@mentio.agency?subject=" +
          encodeURIComponent(cfg.subject + " " + d) + "&body=" +
          encodeURIComponent(cfg.body + " " + d);
      });
    });
  });
})();
