#!/usr/bin/env python3
"""Крок 1 аудита: founder/Person разметка + блок «Кто за этим стоит» + подписи автора."""
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent
NAME = "Oleksandr Motornyy"
LINKEDIN = "https://www.linkedin.com/in/oleksandr-motornyy-7b9473169/"
PERSON_ID = "https://mentio.agency/#founder"

PERSON = {
    "@type": "Person",
    "@id": PERSON_ID,
    "name": NAME,
    "jobTitle": "Founder & GEO Consultant",
    "url": "https://mentio.agency/#founder",
    "sameAs": [LINKEDIN],
    "worksFor": {"@id": "https://mentio.agency/#org"},
    "knowsAbout": [
        "Generative Engine Optimization",
        "AI search visibility",
        "Schema.org structured data",
        "llms.txt",
    ],
}

# ---------------------------------------------------------------- homepages

L10N = {
    "index.html": dict(
        lang="en",
        kicker="Who's behind this",
        h2="You'll be working with me directly",
        role="Founder &amp; GEO Consultant",
        bio="I run Mentio. Every method that goes into a client audit is tested on this "
            "site first — including the uncomfortable part: we published our own audit, "
            "starting score and all (53/100), plus everything we fixed to move up. Order "
            "an audit and you're dealing with me, not an account manager.",
        link=f"{NAME} on LinkedIn →",
    ),
    "ua/index.html": dict(
        lang="uk",
        kicker="Хто за цим стоїть",
        h2="Ви працюватимете напряму зі мною",
        role="Засновник і GEO-консультант",
        bio="Я веду Mentio. Кожен метод, який потрапляє в клієнтський аудит, спершу "
            "перевіряється на цьому сайті — разом із незручною частиною: ми опублікували "
            "власний аудит із початковою оцінкою 53/100 і всім, що виправили. Замовляючи "
            "аудит, ви спілкуєтесь зі мною, а не з менеджером.",
        link=f"{NAME} у LinkedIn →",
    ),
    "de/index.html": dict(
        lang="de",
        kicker="Wer dahintersteht",
        h2="Sie arbeiten direkt mit mir",
        role="Gründer &amp; GEO-Berater",
        bio="Ich führe Mentio. Jede Methode, die in ein Kunden-Audit einfließt, wird "
            "zuerst auf dieser Website getestet — inklusive des unangenehmen Teils: Wir "
            "haben unser eigenes Audit veröffentlicht, mit dem Startwert 53/100 und allem, "
            "was wir behoben haben. Wer ein Audit bucht, spricht mit mir, nicht mit einem "
            "Account Manager.",
        link=f"{NAME} auf LinkedIn →",
    ),
    "fr/index.html": dict(
        lang="fr",
        kicker="Qui est derrière",
        h2="Vous travaillez directement avec moi",
        role="Fondateur &amp; consultant GEO",
        bio="Je dirige Mentio. Chaque méthode utilisée dans un audit client est d'abord "
            "testée sur ce site — y compris la partie inconfortable : nous avons publié "
            "notre propre audit, note de départ comprise (53/100), et tout ce que nous "
            "avons corrigé. En commandant un audit, vous échangez avec moi, pas avec un "
            "commercial.",
        link=f"{NAME} sur LinkedIn →",
    ),
    "pl/index.html": dict(
        lang="pl",
        kicker="Kto za tym stoi",
        h2="Będziesz pracować bezpośrednio ze mną",
        role="Założyciel i konsultant GEO",
        bio="Prowadzę Mentio. Każda metoda, która trafia do audytu klienta, jest najpierw "
            "testowana na tej stronie — łącznie z niewygodną częścią: opublikowaliśmy "
            "własny audyt z wynikiem wyjściowym 53/100 i wszystkim, co naprawiliśmy. "
            "Zamawiając audyt, rozmawiasz ze mną, a nie z opiekunem klienta.",
        link=f"{NAME} na LinkedIn →",
    ),
    "es/index.html": dict(
        lang="es",
        kicker="Quién está detrás",
        h2="Trabajarás directamente conmigo",
        role="Fundador y consultor GEO",
        bio="Dirijo Mentio. Cada método que entra en una auditoría de cliente se prueba "
            "primero en esta web — incluida la parte incómoda: publicamos nuestra propia "
            "auditoría con la puntuación inicial (53/100) y todo lo que corregimos. Al "
            "pedir una auditoría hablas conmigo, no con un gestor de cuentas.",
        link=f"{NAME} en LinkedIn →",
    ),
}

SECTION = """<section id="founder">
  <div class="wrap">
    <p class="kicker">{kicker}</p>
    <h2>{h2}</h2>
    <div class="founder-card card">
      <div class="founder-ava" aria-hidden="true">OM</div>
      <div>
        <h3>{name}</h3>
        <p class="founder-role">{role}</p>
        <p class="bio">{bio}</p>
        <a class="founder-link" href="{li}" rel="author noopener" target="_blank">{link}</a>
      </div>
    </div>
  </div>
</section>

"""

FOUNDER_JSONLD = (
    '      "founder": {"@type": "Person", "@id": "https://mentio.agency/#founder", '
    '"name": "Oleksandr Motornyy", "jobTitle": "Founder & GEO Consultant", '
    '"url": "https://mentio.agency/#founder", '
    '"sameAs": ["https://www.linkedin.com/in/oleksandr-motornyy-7b9473169/"], '
    '"knowsAbout": ["Generative Engine Optimization", "AI search visibility", '
    '"Schema.org structured data", "llms.txt"]},\n'
)

changed = []

for rel, t in L10N.items():
    p = ROOT / rel
    s = p.read_text(encoding="utf-8")

    # 1. JSON-LD: founder внутрь Organization
    if '"@id": "https://mentio.agency/#founder"' not in s:
        anchor = '      "foundingDate": "2026",\n'
        assert anchor in s, f"no foundingDate anchor in {rel}"
        s = s.replace(anchor, anchor + FOUNDER_JSONLD, 1)

    # 2. видимый блок перед финальной секцией
    if 'id="founder"' not in s:
        anchor = '<section class="final"'
        assert anchor in s, f"no final section in {rel}"
        block = SECTION.format(name=NAME, li=LINKEDIN, **t)
        s = s.replace(anchor, block + anchor, 1)

    p.write_text(s, encoding="utf-8")
    changed.append(rel)

# ------------------------------------------------------------------- статьи

posts = sorted(ROOT.glob("blog/*/index.html")) + sorted(ROOT.glob("ua/blog/*/index.html"))
posts = [p for p in posts if p.parent.name != "blog"]

BYLINE = (
    f'<a class="byline" href="{LINKEDIN}" rel="author noopener" target="_blank">{NAME}</a>'
)

for p in posts:
    s = p.read_text(encoding="utf-8")

    # 1. видимая подпись автора вместо «Mentio»
    s = s.replace('</a> · Mentio · ', f'</a> · {BYLINE} · ', 1)

    # 2. JSON-LD
    m = re.search(r'(<script type="application/ld\+json">)(.*?)(</script>)', s, re.S)
    data = json.loads(m.group(2))
    graph = data["@graph"]

    if not any(n.get("@id") == PERSON_ID for n in graph):
        for n in graph:
            if n.get("@type") == "Article":
                n["author"] = {"@id": PERSON_ID}
            if n.get("@type") == "Organization":
                n["founder"] = {"@id": PERSON_ID}
        idx = next(i for i, n in enumerate(graph) if n.get("@type") == "Article")
        graph.insert(idx + 1, PERSON)

    body = "\n" + json.dumps(data, indent=1, ensure_ascii=False) + "\n"
    s = s[: m.start(2)] + body + s[m.end(2) :]
    p.write_text(s, encoding="utf-8")
    changed.append(str(p.relative_to(ROOT)))

print(f"обновлено файлов: {len(changed)}")
for c in changed:
    print("  ", c)
