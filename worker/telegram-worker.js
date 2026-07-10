/**
 * Mentio lead relay — Cloudflare Worker
 * Receives POST from mentio.agency forms and forwards leads to a Telegram chat.
 * Secrets (set in Worker settings, never in code):
 *   TG_TOKEN — Telegram bot token from @BotFather
 *   TG_CHAT  — your chat id (get it from @userinfobot)
 */

const ALLOWED_ORIGINS = ["https://mentio.agency", "https://www.mentio.agency"];

function esc(s) {
  return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

export default {
  async fetch(request, env) {
    const origin = request.headers.get("Origin") || "";
    const cors = {
      "Access-Control-Allow-Origin": ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0],
      "Access-Control-Allow-Methods": "POST, OPTIONS",
      "Access-Control-Allow-Headers": "Content-Type",
    };

    if (request.method === "OPTIONS") return new Response(null, { status: 204, headers: cors });
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

    if (!tg.ok) return new Response("Relay error", { status: 502, headers: cors });
    return new Response("ok", { status: 200, headers: cors });
  },
};
