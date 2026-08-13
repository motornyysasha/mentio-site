#!/usr/bin/env python3
"""Render the link-preview cards from tools/og-card.html into assets/og*.png.

One card per locale (1200x630). All copy is lifted verbatim from the locale's
own index.html — hero headline, hero sub, buy-button price, checkout delivery
line, crane caption — so the preview can never drift from the page it links to.

Rendered at 2x with headless Chrome, then downsampled: 1x rasterisation is
visibly coarser, and every social platform rescales the card again anyway.

Usage: python3 make-og.py            # all locales
       python3 make-og.py ua de      # just these
"""
import pathlib
import subprocess
import sys
import tempfile
import time

ROOT = pathlib.Path(__file__).resolve().parent
TPL = ROOT / "tools" / "og-card.html"
W, H = 1200, 630

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# lead = ink part of the h1, hot = the vermilion phrase the brush underlines
# (the split matches .grad-text on each locale's hero). h1/sub sizes are tuned
# per locale so every card lands on the same number of lines.
LOCALES = {
    "en": {
        "out": "og.png",
        "lang": "en",
        "lead": "Your customers are asking AI. Is it",
        "hot": "answering with you?",
        "sub": "ChatGPT, Perplexity and Google AI Overviews cite only a handful of businesses. Mentio makes sure yours is one of them.",
        "price": "Audit €99",
        "days": "Report in 2 business days",
        "cap": "From a flat sheet, a crane. From an invisible site, a cited one.",
        "h1": "60px",
        "subsize": "22px",
    },
    "ua": {
        "out": "og-ua.png",
        "lang": "uk",
        "lead": "Ваші клієнти вже питають AI. Чи є",
        "hot": "ви у відповіді?",
        "sub": "ChatGPT, Perplexity та Google AI Overviews цитують лише кілька бізнесів. Mentio робить так, щоб серед них були ви.",
        "price": "Аудит €99",
        "days": "Звіт протягом 2 робочих днів",
        "cap": "З плаского аркуша — журавлик. З невидимого сайту — цитований.",
        "h1": "58px",
        "subsize": "22px",
    },
    "de": {
        "out": "og-de.png",
        "lang": "de",
        "lead": "Ihre Kunden fragen bereits die KI. Sind Sie",
        "hot": "Teil der Antwort?",
        "sub": "ChatGPT, Perplexity und Google AI Overviews zitieren nur eine Handvoll Unternehmen. Mentio sorgt dafür, dass Ihres dazugehört.",
        "price": "Audit 99 €",
        "days": "Bericht in 2 Werktagen",
        "cap": "Aus dem flachen Blatt ein Kranich. Aus der unsichtbaren Website eine zitierte.",
        "h1": "55px",
        "subsize": "21px",
    },
    "fr": {
        "out": "og-fr.png",
        "lang": "fr",
        "lead": "Vos clients interrogent déjà l'IA. Êtes-vous",
        "hot": "dans la réponse ?",
        "sub": "ChatGPT, Perplexity et Google AI Overviews ne citent qu'une poignée d'entreprises. Mentio fait en sorte que la vôtre en fasse partie.",
        "price": "Audit 99 €",
        "days": "Rapport sous 2 jours ouvrés",
        "cap": "D'une feuille plate, une grue. D'un site invisible, un site cité.",
        "h1": "55px",
        "subsize": "21px",
    },
    "pl": {
        "out": "og-pl.png",
        "lang": "pl",
        "lead": "Twoi klienci już pytają AI. Czy jesteś",
        "hot": "w odpowiedzi?",
        "sub": "ChatGPT, Perplexity i Google AI Overviews cytują tylko garstkę firm. Mentio dba o to, by Twoja była wśród nich.",
        "price": "Audyt 99 €",
        "days": "Raport w 2 dni robocze",
        "cap": "Z płaskiej kartki — żuraw. Z niewidzialnej strony — cytowana.",
        "h1": "58px",
        "subsize": "22px",
    },
    "es": {
        "out": "og-es.png",
        "lang": "es",
        "lead": "Tus clientes ya le preguntan a la IA. ¿Estás",
        "hot": "en la respuesta?",
        "sub": "ChatGPT, Perplexity y Google AI Overviews citan solo a un puñado de negocios. Mentio se asegura de que el tuyo sea uno de ellos.",
        "price": "Auditoría 99 €",
        "days": "Informe en 2 días laborables",
        "cap": "De una hoja plana, una grulla. De una web invisible, una citada.",
        "h1": "50px",
        "subsize": "21px",
    },
}


def render(html_path, out_path, tmp):
    """Screenshot one filled template. Chrome 151 never exits on the legacy
    --headless, so use --headless=new and poll for the file instead."""
    shot = pathlib.Path(tmp) / "shot.png"
    if shot.exists():
        shot.unlink()
    proc = subprocess.Popen(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            "--no-sandbox",
            "--force-device-scale-factor=2",
            # local @font-face files load over file:// only with this
            "--allow-file-access-from-files",
            f"--user-data-dir={tmp}/profile",
            f"--window-size={W},{H}",
            f"--screenshot={shot}",
            html_path.as_uri(),
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(60):
        if shot.exists() and shot.stat().st_size > 0:
            break
        time.sleep(1)
    proc.terminate()
    if not shot.exists() or shot.stat().st_size == 0:
        sys.exit(f"Chrome produced no screenshot for {out_path.name}")
    subprocess.run(
        ["sips", "-z", str(H), str(W), str(shot), "--out", str(out_path)],
        check=True,
        capture_output=True,
    )


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    if not TPL.exists():
        sys.exit(f"Template missing: {TPL}")

    wanted = sys.argv[1:] or list(LOCALES)
    unknown = [w for w in wanted if w not in LOCALES]
    if unknown:
        sys.exit(f"Unknown locale(s): {', '.join(unknown)}")

    tpl = TPL.read_text(encoding="utf-8")
    with tempfile.TemporaryDirectory() as tmp:
        for code in wanted:
            L = LOCALES[code]
            filled = (
                tpl.replace("{{LANG}}", L["lang"])
                .replace("{{LEAD}}", L["lead"])
                .replace("{{HOT}}", L["hot"])
                .replace("{{SUB}}", L["sub"])
                .replace("{{PRICE}}", L["price"])
                .replace("{{DAYS}}", L["days"])
                .replace("{{CAP}}", L["cap"])
                .replace("{{H1SIZE}}", L["h1"])
                .replace("{{SUBSIZE}}", L["subsize"])
            )
            # the filled copy must sit next to the template: the @font-face
            # srcs are relative (../assets/fonts/…)
            work = TPL.parent / f".og-{code}.tmp.html"
            work.write_text(filled, encoding="utf-8")
            out = ROOT / "assets" / L["out"]
            try:
                render(work, out, tmp)
            finally:
                work.unlink(missing_ok=True)
            print(f"  {code}: assets/{L['out']} ({out.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
