/* mentio site.js */
(function () {
  "use strict";
  var reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = window.matchMedia("(pointer: fine)").matches;
  function sleep(ms) { return new Promise(function (r) { setTimeout(r, ms); }); }

  /* ---------- language switcher (CSP-safe, replaces inline onchange) ---------- */
  document.querySelectorAll("select.lang-select").forEach(function (sel) {
    sel.addEventListener("change", function () {
      if (this.value) location.href = this.value;
    });
  });

  /* ---------- mobile nav burger (panel built here: no-JS keeps today's compact bar) ---------- */
  (function () {
    var nav = document.querySelector("nav");
    if (!nav) return;
    var linksBox = nav.querySelector(".nav-links");
    var links = nav.querySelectorAll(".nav-links a:not(.nav-cta)");
    if (!linksBox || !links.length) return;
    var MENU_LABEL = { en: "Menu", uk: "Меню", de: "Menü", fr: "Menu", pl: "Menu", es: "Menú" };
    var burger = document.createElement("button");
    burger.className = "nav-burger";
    burger.setAttribute("aria-expanded", "false");
    burger.setAttribute("aria-label", MENU_LABEL[document.documentElement.lang] || "Menu");
    burger.innerHTML = '<svg width="20" height="20" viewBox="0 0 20 20" fill="none" aria-hidden="true"><path d="M3 5h14M3 10h14M3 15h14" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>';
    var panel = document.createElement("div");
    panel.className = "nav-panel";
    links.forEach(function (a) { panel.appendChild(a.cloneNode(true)); });
    var cta = linksBox.querySelector('.nav-cta');
    if (cta) { linksBox.insertBefore(burger, cta); } else { linksBox.appendChild(burger); }
    nav.appendChild(panel);
    function close() {
      nav.classList.remove("nav-open");
      burger.setAttribute("aria-expanded", "false");
    }
    burger.addEventListener("click", function () {
      var open = nav.classList.toggle("nav-open");
      burger.setAttribute("aria-expanded", open ? "true" : "false");
    });
    panel.addEventListener("click", function (e) { if (e.target.closest("a")) close(); });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") close(); });
  })();

  /* ---------- print-in: sections type themselves onto the tube ---------- */
  if (!reduced && "IntersectionObserver" in window) {
    var targets = document.querySelectorAll(".card, .step, details, .lead, section h2, .kicker");
    var groups = {};
    targets.forEach(function (el) {
      el.classList.add("pline");
      var key = el.parentElement ? Array.prototype.indexOf.call(document.querySelectorAll("section, header"), el.closest("section, header")) : 0;
      groups[key] = groups[key] || [];
      groups[key].push(el);
      el.style.animationDelay = Math.min(groups[key].length - 1, 5) * 90 + "ms";
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("in");
          e.target.addEventListener("animationend", function h() {
            e.target.classList.remove("pline", "in");
            e.target.style.animationDelay = "";
            e.target.removeEventListener("animationend", h);
          });
          io.unobserve(e.target);
        }
      });
    }, { threshold: 0.12, rootMargin: "0px 0px -40px 0px" });
    targets.forEach(function (el) { io.observe(el); });
  }

  /* ---------- lead delivery ---------- */
  var LEAD_ENDPOINT = window.LEAD_ENDPOINT || "https://cool-waterfall-a3ce.motornyysasha.workers.dev";
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
  function contactValid(c) {
    return /@/.test(c) || /t\.me\//i.test(c) || /^\+?[\d\s()-]{7,}$/.test(c);
  }
  var SCAN_LL_LANG = document.documentElement.lang;
  window.__mentioLead = { enabled: function () { return !!LEAD_ENDPOINT; }, submit: submitLead, contactValid: contactValid };

  /* ---------- CTA links scroll to scanner and focus it ---------- */
  document.querySelectorAll('a[href="#check"]').forEach(function (a) {
    a.addEventListener("click", function () {
      var inp = document.querySelector(".scan-form input");
      if (inp) setTimeout(function () { inp.focus({ preventScroll: true }); }, 650);
    });
  });

  /* ---------- site scanner (real basic check via Worker /scan) ---------- */
  var SCAN_L10N = {
    en: {
      reset: "Check another site",
      invalidContact: "Enter an email or @handle so we can reply",
      goodTitle: "Already good",
      badTitle: "Critical \u2014 fix these",
      lead: "Want the full report with every fix, step by step? Leave a contact:",
      unreachable: "Couldn't reach the site \u2014 check the spelling. If it's correct, the site may be blocking robots entirely (AI assistants included).",
      good: {
        aiAccess: "AI crawlers (GPTBot, ClaudeBot, PerplexityBot) are allowed in",
        llms: "llms.txt found \u2014 AI gets a machine-readable summary",
        jsonld: "Structured data (Schema.org) is present",
        robots: "robots.txt in place",
        sitemap: "Sitemap declared for crawlers",
        metaDesc: "Meta description is set",
        basics: "Title, H1 and mobile viewport are in place"
      },
      bad: {
        allBlocked: "robots.txt blocks ALL crawlers \u2014 the site is invisible to search and AI assistants",
        aiBlocked: "AI crawlers are blocked in robots.txt ({list}) \u2014 those assistants can't read the site",
        llms: "No llms.txt \u2014 AI has no quick map of the site",
        jsonld: "No structured data (Schema.org) \u2014 AI can't verify who you are",
        robots: "No robots.txt \u2014 crawler access is undefined",
        sitemap: "No sitemap declared \u2014 crawlers may miss pages",
        metaDesc: "No meta description \u2014 AI and Google write their own snippet for you",
        basics: "Missing basics: {list}", title: "title", h1: "H1", viewport: "mobile viewport"
      }
    },
    uk: {
      reset: "Перевірити інший сайт",
      invalidContact: "Вкажіть email або @нік, щоб ми могли відповісти",
      goodTitle: "\u0412\u0436\u0435 \u0434\u043e\u0431\u0440\u0435",
      badTitle: "\u041a\u0440\u0438\u0442\u0438\u0447\u043d\u043e \u2014 \u0442\u0440\u0435\u0431\u0430 \u0432\u0438\u043f\u0440\u0430\u0432\u0438\u0442\u0438",
      lead: "\u0425\u043e\u0447\u0435\u0442\u0435 \u043f\u043e\u0432\u043d\u0438\u0439 \u0437\u0432\u0456\u0442 \u0437 \u0443\u0441\u0456\u043c\u0430 \u0432\u0438\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043d\u044f\u043c\u0438, \u043a\u0440\u043e\u043a \u0437\u0430 \u043a\u0440\u043e\u043a\u043e\u043c? \u0417\u0430\u043b\u0438\u0448\u0442\u0435 \u043a\u043e\u043d\u0442\u0430\u043a\u0442:",
      unreachable: "\u041d\u0435 \u0432\u0434\u0430\u043b\u043e\u0441\u044f \u0432\u0456\u0434\u043a\u0440\u0438\u0442\u0438 \u0441\u0430\u0439\u0442 \u2014 \u043f\u0435\u0440\u0435\u0432\u0456\u0440\u0442\u0435 \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u043d\u044f. \u042f\u043a\u0449\u043e \u0432\u0441\u0435 \u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e, \u0441\u0430\u0439\u0442 \u043c\u043e\u0436\u0435 \u043f\u043e\u0432\u043d\u0456\u0441\u0442\u044e \u0431\u043b\u043e\u043a\u0443\u0432\u0430\u0442\u0438 \u0440\u043e\u0431\u043e\u0442\u0456\u0432 (\u0440\u0430\u0437\u043e\u043c \u0437 AI-\u0430\u0441\u0438\u0441\u0442\u0435\u043d\u0442\u0430\u043c\u0438).",
      good: {
        aiAccess: "AI-\u043a\u0440\u0430\u0443\u043b\u0435\u0440\u0438 (GPTBot, ClaudeBot, PerplexityBot) \u043c\u0430\u044e\u0442\u044c \u0434\u043e\u0441\u0442\u0443\u043f",
        llms: "\u0404 llms.txt \u2014 AI \u043e\u0442\u0440\u0438\u043c\u0443\u0454 \u043c\u0430\u0448\u0438\u043d\u043e\u0437\u0447\u0438\u0442\u0443\u0432\u0430\u043d\u0438\u0439 \u043e\u043f\u0438\u0441",
        jsonld: "\u0404 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043e\u0432\u0430\u043d\u0456 \u0434\u0430\u043d\u0456 (Schema.org)",
        robots: "\u0404 robots.txt",
        sitemap: "Sitemap \u043e\u0433\u043e\u043b\u043e\u0448\u0435\u043d\u043e \u0434\u043b\u044f \u043a\u0440\u0430\u0443\u043b\u0435\u0440\u0456\u0432",
        metaDesc: "Meta description \u0437\u0430\u043f\u043e\u0432\u043d\u0435\u043d\u043e",
        basics: "Title, H1 \u0442\u0430 \u043c\u043e\u0431\u0456\u043b\u044c\u043d\u0438\u0439 viewport \u043d\u0430 \u043c\u0456\u0441\u0446\u0456"
      },
      bad: {
        allBlocked: "robots.txt \u0431\u043b\u043e\u043a\u0443\u0454 \u0412\u0421\u0406\u0425 \u0440\u043e\u0431\u043e\u0442\u0456\u0432 \u2014 \u0441\u0430\u0439\u0442 \u043d\u0435\u0432\u0438\u0434\u0438\u043c\u0438\u0439 \u0434\u043b\u044f \u043f\u043e\u0448\u0443\u043a\u0443 \u0442\u0430 AI",
        aiBlocked: "AI-\u043a\u0440\u0430\u0443\u043b\u0435\u0440\u0438 \u0437\u0430\u0431\u043b\u043e\u043a\u043e\u0432\u0430\u043d\u0456 \u0432 robots.txt ({list}) \u2014 \u0446\u0456 \u0430\u0441\u0438\u0441\u0442\u0435\u043d\u0442\u0438 \u043d\u0435 \u0447\u0438\u0442\u0430\u044e\u0442\u044c \u0441\u0430\u0439\u0442",
        llms: "\u041d\u0435\u043c\u0430\u0454 llms.txt \u2014 \u0432 AI \u043d\u0435\u043c\u0430\u0454 \u0448\u0432\u0438\u0434\u043a\u043e\u0457 \u043c\u0430\u043f\u0438 \u0441\u0430\u0439\u0442\u0443",
        jsonld: "\u041d\u0435\u043c\u0430\u0454 \u0441\u0442\u0440\u0443\u043a\u0442\u0443\u0440\u043e\u0432\u0430\u043d\u0438\u0445 \u0434\u0430\u043d\u0438\u0445 (Schema.org) \u2014 AI \u043d\u0435 \u043c\u043e\u0436\u0435 \u043f\u0456\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0438, \u0445\u0442\u043e \u0432\u0438",
        robots: "\u041d\u0435\u043c\u0430\u0454 robots.txt \u2014 \u0434\u043e\u0441\u0442\u0443\u043f \u043a\u0440\u0430\u0443\u043b\u0435\u0440\u0456\u0432 \u043d\u0435 \u0432\u0438\u0437\u043d\u0430\u0447\u0435\u043d\u043e",
        sitemap: "Sitemap \u043d\u0435 \u043e\u0433\u043e\u043b\u043e\u0448\u0435\u043d\u043e \u2014 \u043a\u0440\u0430\u0443\u043b\u0435\u0440\u0438 \u043c\u043e\u0436\u0443\u0442\u044c \u043f\u0440\u043e\u043f\u0443\u0441\u0442\u0438\u0442\u0438 \u0441\u0442\u043e\u0440\u0456\u043d\u043a\u0438",
        metaDesc: "\u041d\u0435\u043c\u0430\u0454 meta description \u2014 AI \u0456 Google \u043f\u0438\u0448\u0443\u0442\u044c \u043e\u043f\u0438\u0441 \u0437\u0430 \u0432\u0430\u0441",
        basics: "\u0411\u0440\u0430\u043a\u0443\u0454 \u0431\u0430\u0437\u043e\u0432\u0438\u0445 \u0440\u0435\u0447\u0435\u0439: {list}", title: "title", h1: "H1", viewport: "\u043c\u043e\u0431\u0456\u043b\u044c\u043d\u0438\u0439 viewport"
      }
    },
    de: {
      reset: "Weitere Website prüfen",
      invalidContact: "E-Mail oder @Handle angeben, damit wir antworten können",
      goodTitle: "Schon gut",
      badTitle: "Kritisch \u2014 bitte beheben",
      lead: "M\u00f6chten Sie den vollst\u00e4ndigen Bericht mit allen Korrekturen? Kontakt hinterlassen:",
      unreachable: "Website nicht erreichbar \u2014 bitte Schreibweise pr\u00fcfen. Falls korrekt, blockiert die Website wom\u00f6glich alle Robots (auch KI-Assistenten).",
      good: {
        aiAccess: "KI-Crawler (GPTBot, ClaudeBot, PerplexityBot) sind zugelassen",
        llms: "llms.txt gefunden \u2014 KI erh\u00e4lt eine maschinenlesbare \u00dcbersicht",
        jsonld: "Strukturierte Daten (Schema.org) vorhanden",
        robots: "robots.txt vorhanden",
        sitemap: "Sitemap f\u00fcr Crawler deklariert",
        metaDesc: "Meta-Description gesetzt",
        basics: "Title, H1 und mobiler Viewport vorhanden"
      },
      bad: {
        allBlocked: "robots.txt blockiert ALLE Crawler \u2014 die Website ist f\u00fcr Suche und KI unsichtbar",
        aiBlocked: "KI-Crawler sind in robots.txt blockiert ({list}) \u2014 diese Assistenten k\u00f6nnen die Website nicht lesen",
        llms: "Keine llms.txt \u2014 KI hat keine schnelle \u00dcbersicht der Website",
        jsonld: "Keine strukturierten Daten (Schema.org) \u2014 KI kann nicht pr\u00fcfen, wer Sie sind",
        robots: "Keine robots.txt \u2014 Crawler-Zugriff ist undefiniert",
        sitemap: "Keine Sitemap deklariert \u2014 Crawler k\u00f6nnen Seiten \u00fcbersehen",
        metaDesc: "Keine Meta-Description \u2014 KI und Google texten selbst f\u00fcr Sie",
        basics: "Basics fehlen: {list}", title: "Title", h1: "H1", viewport: "mobiler Viewport"
      }
    },
    fr: {
      reset: "Vérifier un autre site",
      invalidContact: "Indiquez un e-mail ou un @pseudo pour qu'on puisse répondre",
      goodTitle: "D\u00e9j\u00e0 en place",
      badTitle: "Critique \u2014 \u00e0 corriger",
      lead: "Envie du rapport complet avec toutes les corrections ? Laissez un contact :",
      unreachable: "Impossible d'atteindre le site \u2014 v\u00e9rifiez l'orthographe. Si elle est correcte, le site bloque peut-\u00eatre tous les robots (assistants IA compris).",
      good: {
        aiAccess: "Les crawlers IA (GPTBot, ClaudeBot, PerplexityBot) sont autoris\u00e9s",
        llms: "llms.txt trouv\u00e9 \u2014 l'IA re\u00e7oit un r\u00e9sum\u00e9 lisible par machine",
        jsonld: "Donn\u00e9es structur\u00e9es (Schema.org) pr\u00e9sentes",
        robots: "robots.txt en place",
        sitemap: "Sitemap d\u00e9clar\u00e9 pour les crawlers",
        metaDesc: "Meta description renseign\u00e9e",
        basics: "Title, H1 et viewport mobile en place"
      },
      bad: {
        allBlocked: "robots.txt bloque TOUS les robots \u2014 le site est invisible pour la recherche et l'IA",
        aiBlocked: "Les crawlers IA sont bloqu\u00e9s dans robots.txt ({list}) \u2014 ces assistants ne peuvent pas lire le site",
        llms: "Pas de llms.txt \u2014 l'IA n'a pas de plan rapide du site",
        jsonld: "Pas de donn\u00e9es structur\u00e9es (Schema.org) \u2014 l'IA ne peut pas v\u00e9rifier qui vous \u00eates",
        robots: "Pas de robots.txt \u2014 l'acc\u00e8s des crawlers est ind\u00e9fini",
        sitemap: "Pas de sitemap d\u00e9clar\u00e9 \u2014 les crawlers peuvent manquer des pages",
        metaDesc: "Pas de meta description \u2014 l'IA et Google \u00e9crivent \u00e0 votre place",
        basics: "Bases manquantes : {list}", title: "title", h1: "H1", viewport: "viewport mobile"
      }
    },
    pl: {
      reset: "Sprawdź inną stronę",
      invalidContact: "Podaj e-mail lub @nick, żebyśmy mogli odpowiedzieć",
      goodTitle: "Ju\u017c dobrze",
      badTitle: "Krytyczne \u2014 do poprawy",
      lead: "Chcesz pe\u0142ny raport ze wszystkimi poprawkami? Zostaw kontakt:",
      unreachable: "Nie uda\u0142o si\u0119 otworzy\u0107 strony \u2014 sprawd\u017a pisowni\u0119. Je\u015bli jest poprawna, strona mo\u017ce ca\u0142kowicie blokowa\u0107 roboty (w tym asystent\u00f3w AI).",
      good: {
        aiAccess: "Crawlery AI (GPTBot, ClaudeBot, PerplexityBot) maj\u0105 dost\u0119p",
        llms: "Znaleziono llms.txt \u2014 AI dostaje maszynowy opis strony",
        jsonld: "Dane strukturalne (Schema.org) obecne",
        robots: "Jest robots.txt",
        sitemap: "Sitemap zadeklarowana dla crawler\u00f3w",
        metaDesc: "Meta description uzupe\u0142nione",
        basics: "Title, H1 i mobilny viewport na miejscu"
      },
      bad: {
        allBlocked: "robots.txt blokuje WSZYSTKIE roboty \u2014 strona jest niewidoczna dla wyszukiwarek i AI",
        aiBlocked: "Crawlery AI s\u0105 zablokowane w robots.txt ({list}) \u2014 ci asystenci nie czytaj\u0105 strony",
        llms: "Brak llms.txt \u2014 AI nie ma szybkiej mapy strony",
        jsonld: "Brak danych strukturalnych (Schema.org) \u2014 AI nie mo\u017ce zweryfikowa\u0107, kim jeste\u015b",
        robots: "Brak robots.txt \u2014 dost\u0119p crawler\u00f3w jest nieokre\u015blony",
        sitemap: "Brak sitemapy \u2014 crawlery mog\u0105 pomin\u0105\u0107 podstrony",
        metaDesc: "Brak meta description \u2014 AI i Google pisz\u0105 opis za Ciebie",
        basics: "Brakuje podstaw: {list}", title: "title", h1: "H1", viewport: "mobilny viewport"
      }
    },
    es: {
      reset: "Comprobar otro sitio",
      invalidContact: "Indica un email o @usuario para que podamos responder",
      goodTitle: "Ya est\u00e1 bien",
      badTitle: "Cr\u00edtico \u2014 hay que corregir",
      lead: "\u00bfQuieres el informe completo con todas las correcciones? Deja un contacto:",
      unreachable: "No se pudo acceder al sitio \u2014 revisa la ortograf\u00eda. Si es correcta, puede que el sitio bloquee todos los robots (asistentes de IA incluidos).",
      good: {
        aiAccess: "Los crawlers de IA (GPTBot, ClaudeBot, PerplexityBot) tienen acceso",
        llms: "llms.txt encontrado \u2014 la IA recibe un resumen legible por m\u00e1quina",
        jsonld: "Datos estructurados (Schema.org) presentes",
        robots: "robots.txt en su sitio",
        sitemap: "Sitemap declarado para los crawlers",
        metaDesc: "Meta description completada",
        basics: "Title, H1 y viewport m\u00f3vil en su sitio"
      },
      bad: {
        allBlocked: "robots.txt bloquea TODOS los robots \u2014 el sitio es invisible para buscadores e IA",
        aiBlocked: "Los crawlers de IA est\u00e1n bloqueados en robots.txt ({list}) \u2014 esos asistentes no pueden leer el sitio",
        llms: "No hay llms.txt \u2014 la IA no tiene un mapa r\u00e1pido del sitio",
        jsonld: "No hay datos estructurados (Schema.org) \u2014 la IA no puede verificar qui\u00e9n eres",
        robots: "No hay robots.txt \u2014 el acceso de los crawlers queda indefinido",
        sitemap: "No hay sitemap declarado \u2014 los crawlers pueden saltarse p\u00e1ginas",
        metaDesc: "No hay meta description \u2014 la IA y Google escriben por ti",
        basics: "Faltan b\u00e1sicos: {list}", title: "title", h1: "H1", viewport: "viewport m\u00f3vil"
      }
    }
  };

  function buildScanResults(checks, L) {
    var goods = [], bads = [];
    if (!checks.reachable) return { goods: goods, bads: bads, unreachable: true };

    // goods, most impressive first
    if (checks.robotsFound && !checks.allBlocked && checks.aiBlocked.length === 0) goods.push(L.good.aiAccess);
    if (checks.llms) goods.push(L.good.llms);
    if (checks.jsonld) goods.push(L.good.jsonld);
    if (checks.robotsFound && checks.sitemap) goods.push(L.good.sitemap);
    else if (checks.robotsFound) goods.push(L.good.robots);
    if (checks.metaDesc) goods.push(L.good.metaDesc);
    if (checks.title && checks.h1 && checks.viewport) goods.push(L.good.basics);

    // criticals, most severe first
    if (checks.allBlocked) bads.push(L.bad.allBlocked);
    else if (checks.aiBlocked.length) bads.push(L.bad.aiBlocked.replace("{list}", checks.aiBlocked.slice(0, 3).join(", ") + (checks.aiBlocked.length > 3 ? "\u2026" : "")));
    if (!checks.llms) bads.push(L.bad.llms);
    if (!checks.jsonld) bads.push(L.bad.jsonld);
    if (!checks.robotsFound) bads.push(L.bad.robots);
    else if (!checks.sitemap) bads.push(L.bad.sitemap);
    if (!checks.metaDesc) bads.push(L.bad.metaDesc);
    var missing = [];
    if (!checks.title) missing.push(L.bad.title);
    if (!checks.h1) missing.push(L.bad.h1);
    if (!checks.viewport) missing.push(L.bad.viewport);
    if (missing.length) bads.push(L.bad.basics.replace("{list}", missing.join(", ")));

    return { goods: goods.slice(0, 4), bads: bads.slice(0, 3), unreachable: false };
  }

  window.__mentioLead.invalidContact = (SCAN_L10N[document.documentElement.lang] || SCAN_L10N.en).invalidContact;

  /* ---------- boot transcript: the TTY prints itself awake ---------- */
  (function () {
    var body = document.querySelector(".scan-hero .demo-body");
    if (!body) return;
    var boot = document.createElement("div");
    boot.className = "boot";
    boot.setAttribute("aria-hidden", "true");
    ["MENTIO GEO TERMINAL v3.2 — tty1", "link established · ssr ok · 6 locales", ""].forEach(function (txt, i) {
      var p = document.createElement("p");
      if (i === 1) p.className = "ok";
      if (i === 2) {
        p.className = "prompt";
        p.textContent = "> type your domain to begin";
        var cur = document.createElement("span");
        cur.className = "cursor";
        p.appendChild(cur);
      } else {
        p.textContent = txt;
      }
      if (!reduced) {
        p.classList.add("pline", "in");
        p.style.animationDelay = (200 + i * 380) + "ms";
      }
      boot.appendChild(p);
    });
    body.insertBefore(boot, body.firstChild);
  })();

  document.querySelectorAll("form.scan-form").forEach(function (f) {
    var cfg;
    try { cfg = JSON.parse(f.getAttribute("data-cfg")); } catch (e) { return; }
    var L = SCAN_L10N[document.documentElement.lang] || SCAN_L10N.en;
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
    function renderResults(res) {
      var old = f.parentElement.querySelector(".scan-result");
      if (old) old.remove();
      var box = document.createElement("div");
      box.className = "scan-result";
      function addList(title, items, cls) {
        if (!items.length) return;
        var h = document.createElement("p");
        h.className = "sr-title " + cls;
        h.textContent = title;
        box.appendChild(h);
        var ul = document.createElement("ul");
        ul.className = cls;
        items.forEach(function (t) {
          var li = document.createElement("li");
          li.textContent = t;
          ul.appendChild(li);
        });
        box.appendChild(ul);
      }
      addList(L.goodTitle, res.goods, "sr-good");
      addList(L.badTitle, res.bads, "sr-bad");
      if (!reduced) {
        var row = 0;
        box.querySelectorAll(".sr-title, li").forEach(function (el) {
          el.classList.add("pline", "in");
          el.style.animationDelay = (row++ * 140) + "ms";
        });
      }
      f.parentElement.insertBefore(box, status);
    }
    var origPh = input.placeholder, origAria = input.getAttribute("aria-label"), origBtn = btn.textContent;
    var contactValid = window.__mentioLead.contactValid;
    function resetScanner() {
      stage = 1;
      var box = f.parentElement.querySelector(".scan-result");
      if (box) box.remove();
      var chip = f.querySelector(".scan-chip");
      if (chip) chip.remove();
      var rl = f.parentElement.querySelector(".scan-reset");
      if (rl) rl.remove();
      status.before(f);
      f.hidden = false;
      f.classList.remove("invalid");
      status.classList.remove("ok");
      status.textContent = "";
      input.value = "";
      input.placeholder = origPh;
      if (origAria) input.setAttribute("aria-label", origAria);
      input.removeAttribute("inputmode");
      btn.textContent = origBtn;
      btn.disabled = false;
      savedDomain = "";
      input.focus();
    }
    function toContactStage(msg) {
      savedDomain = savedDomain || domainOf();
      stage = 2;
      /* reading order for stage 2: results -> instruction -> contact form -> reset */
      var box = f.parentElement.querySelector(".scan-result");
      if (box) { box.after(status); status.after(f); }
      status.textContent = msg;
      var chip = document.createElement("span");
      chip.className = "scan-chip";
      chip.textContent = "✓ " + savedDomain;
      chip.title = savedDomain;
      f.insertBefore(chip, input);
      input.value = "";
      input.placeholder = cfg.contactPh;
      input.setAttribute("aria-label", cfg.contactPh);
      input.setAttribute("inputmode", "email");
      btn.textContent = cfg.send;
      var rl = document.createElement("button");
      rl.type = "button";
      rl.className = "scan-reset";
      rl.textContent = L.reset;
      f.after(rl);
      rl.addEventListener("click", resetScanner);
      if (box && !reduced) box.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
    input.addEventListener("input", function () { f.classList.remove("invalid"); });
    f.addEventListener("submit", function (e) {
      e.preventDefault();
      if (stage === 2) {
        var contact = input.value.trim();
        if (!contactValid(contact)) { reject(L.invalidContact); return; }
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
      savedDomain = d;

      // real check and step animation run in parallel; results wait for both
      var scanReq = LEAD_ENDPOINT
        ? fetch(LEAD_ENDPOINT + "/scan?domain=" + encodeURIComponent(d))
            .then(function (r) { if (!r.ok) throw new Error("scan " + r.status); return r.json(); })
        : Promise.reject(new Error("no endpoint"));
      var chain = Promise.resolve();
      cfg.steps.forEach(function (s) {
        chain = chain.then(function () { status.textContent = s; return sleep(reduced ? 50 : 950); });
      });

      Promise.all([scanReq.catch(function () { return null; }), chain]).then(function (pair) {
        var data = pair[0];
        status.classList.add("ok");
        btn.disabled = false;
        if (data && data.ok) {
          var res = buildScanResults(data.checks, L);
          if (res.unreachable) {
            status.classList.remove("ok");
            stage = 1;
            status.textContent = L.unreachable;
            input.focus();
            return;
          }
          renderResults(res);
          if (LEAD_ENDPOINT) { toContactStage(L.lead); } else { status.textContent = cfg.done; }
          return;
        }
        // scan endpoint unavailable \u2014 legacy flow
        if (LEAD_ENDPOINT) {
          toContactStage(cfg.doneForm);
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
      if (contact) ok = ok && window.__mentioLead.contactValid(contact.value.trim());
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
      if (!window.__mentioLead.contactValid(contact.value.trim())) {
        contact.classList.add("invalid");
        hint.hidden = false;
        hint.textContent = window.__mentioLead.invalidContact || scanCfg.contactPh || "email";
        contact.focus();
        return;
      }
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
