/**
 * Mentio lead relay + site scanner — Cloudflare Worker
 *
 * POST /        — receives lead JSON from mentio.agency forms, forwards to Telegram
 * GET  /health  — diagnostics: shows whether secrets are visible (never their values)
 * GET  /scan?domain=example.com — real basic GEO check: fetches the target's
 *                 robots.txt, llms.txt and homepage, returns fact flags as JSON.
 *                 All wording/localization happens client-side in site.js.
 *
 * Secrets (set in Worker settings, never in code):
 *   TG_TOKEN — Telegram bot token from @BotFather
 *   TG_CHAT  — your chat id (get it from @userinfobot)
 */

const ALLOWED_ORIGINS = ["https://mentio.agency", "https://www.mentio.agency", "http://localhost:8899"];

const AI_BOTS = ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot", "meta-externalagent"];
const SCAN_UA = "Mozilla/5.0 (compatible; MentioScan/1.0; +https://mentio.agency)";
const FETCH_TIMEOUT = 7000;
const MAX_HTML = 300 * 1024;

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

async function fetchText(url) {
  try {
    const r = await fetch(url, {
      redirect: "follow",
      headers: { "User-Agent": SCAN_UA, "Accept": "text/html,text/plain,*/*" },
      signal: AbortSignal.timeout(FETCH_TIMEOUT),
    });
    const ct = (r.headers.get("Content-Type") || "").toLowerCase();
    let text = "";
    if (r.ok) text = (await r.text()).slice(0, MAX_HTML);
    return { status: r.status, ok: r.ok, ct, text };
  } catch (e) {
    return { status: 0, ok: false, ct: "", text: "" };
  }
}

/* robots.txt: which of the given bots (or "*") have a blanket "Disallow: /" */
function parseRobots(txt, bots) {
  const groups = []; // { agents: [..], disallowAll: bool }
  let cur = null;
  for (const raw of txt.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, "").trim();
    if (!line) continue;
    const m = line.match(/^([a-z-]+)\s*:\s*(.*)$/i);
    if (!m) continue;
    const key = m[1].toLowerCase(), val = m[2].trim();
    if (key === "user-agent") {
      if (!cur || cur.done) { cur = { agents: [], disallowAll: false, done: false }; groups.push(cur); }
      cur.agents.push(val.toLowerCase());
    } else if (cur) {
      if (key === "disallow" || key === "allow") cur.done = true;
      if (key === "disallow" && val === "/") cur.disallowAll = true;
    }
  }
  const blockedBy = (name) => groups.some(g => g.agents.includes(name.toLowerCase()) && g.disallowAll);
  const starBlocked = blockedBy("*");
  const blocked = bots.filter(b => blockedBy(b) || (starBlocked && !groups.some(g => g.agents.includes(b.toLowerCase()) && !g.disallowAll)));
  const sitemap = /^\s*sitemap\s*:/im.test(txt);
  return { blocked, starBlocked, sitemap };
}

function looksHtml(res) {
  return res.ct.includes("text/html") || /^\s*<(!doctype|html)/i.test(res.text);
}

async function scan(domain) {
  const base = "https://" + domain;
  const [home, robots, llms] = await Promise.all([
    fetchText(base + "/"),
    fetchText(base + "/robots.txt"),
    fetchText(base + "/llms.txt"),
  ]);

  const checks = { reachable: home.ok };
  if (home.ok) {
    const h = home.text.toLowerCase();
    checks.title = /<title[^>]*>\s*[^<\s]/.test(h);
    checks.metaDesc = /<meta[^>]+name=["']description["'][^>]+content=["'][^"']+/.test(h) ||
                      /<meta[^>]+content=["'][^"']+["'][^>]+name=["']description["']/.test(h);
    checks.jsonld = h.includes("application/ld+json");
    checks.h1 = /<h1[\s>]/.test(h);
    checks.og = /property=["']og:/.test(h);
    checks.viewport = /<meta[^>]+name=["']viewport["']/.test(h);
  }

  checks.robotsFound = robots.ok && !looksHtml(robots);
  checks.aiBlocked = [];
  checks.allBlocked = false;
  checks.sitemap = false;
  if (checks.robotsFound) {
    const r = parseRobots(robots.text, AI_BOTS);
    checks.aiBlocked = r.blocked;
    checks.allBlocked = r.starBlocked;
    checks.sitemap = r.sitemap;
  }
  checks.llms = llms.ok && !looksHtml(llms);
  return checks;
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };
    const json = (obj, status) => new Response(JSON.stringify(obj), {
      status: status || 200, headers: { ...cors, "Content-Type": "application/json" },
    });

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });

    if (request.method === "GET") {
      const url = new URL(request.url);

      if (url.pathname === "/scan") {
        const domain = String(url.searchParams.get("domain") || "").trim().toLowerCase()
          .replace(/^https?:\/\//, "").replace(/\/.*$/, "");
        // hostname only, no IP literals / localhost — this worker must not probe private hosts
        if (!/^[a-z0-9Ѐ-ӿ-]+(\.[a-z0-9Ѐ-ӿ-]+)+$/i.test(domain) ||
            /^(\d{1,3}\.){3}\d{1,3}$/.test(domain) || domain.endsWith(".localhost")) {
          return json({ ok: false, error: "bad domain" }, 400);
        }
        const checks = await scan(domain);
        return json({ ok: true, domain, checks });
      }

      // Diagnostics (/, /health)
      return json({ ok: true, hasToken: Boolean(env.TG_TOKEN), hasChat: Boolean(env.TG_CHAT) });
    }

    if (request.method !== "POST") return new Response("Method not allowed", { status: 405, headers: cors });

    let d;
    try { d = await request.json(); } catch { return new Response("Bad JSON", { status: 400, headers: cors }); }

    const domain = String(d.domain || "").trim().slice(0, 120);
    const contact = String(d.contact || "").trim().slice(0, 200);
    const type = String(d.type || "lead").slice(0, 20);
    const lang = String(d.lang || "").slice(0, 8);
    const page = String(d.page || "").slice(0, 120);
    const score = d.score != null ? parseInt(d.score, 10) : null;

    if (!domain || !contact) return new Response("Missing fields", { status: 400, headers: cors });

    const lines = [
      "\u{1F525} <b>Новий лід з mentio.agency</b>",
      "\u{1F310} Сайт: <code>" + esc(domain) + "</code>",
      "\u{1F4EC} Контакт: " + esc(contact),
      Number.isFinite(score) ? "\u{1F4CA} AI Visibility Score: <b>" + score + "/100</b>" : null,
      "\u{1F3F7} Джерело: " + (type === "quiz" ? "тест AI Visibility" : "сканер сайту"),
      lang ? "\u{1F30D} Мова сторінки: " + esc(lang) + (page ? " (" + esc(page) + ")" : "") : null,
    ].filter(Boolean).join("\n");

    const tg = await fetch("https://api.telegram.org/bot" + env.TG_TOKEN + "/sendMessage", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ chat_id: env.TG_CHAT, text: lines, parse_mode: "HTML" }),
    });

    if (!tg.ok) {
      // Pass Telegram's own error through so the cause is visible (e.g. "chat not found", "Unauthorized")
      var detail = "";
      try { detail = (await tg.json()).description || ""; } catch (e) {}
      return new Response("Relay error: " + tg.status + " " + detail, { status: 502, headers: cors });
    }
    return new Response("ok", { status: 200, headers: cors });
  },
};
