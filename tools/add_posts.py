#!/usr/bin/env python3
"""Add new blog posts (EN+UA) from the shared article template and re-date the whole blog
as an editorial calendar. Run from the site root: python3 tools/add_posts.py"""
import pathlib, re, json

SITE = pathlib.Path(__file__).resolve().parent.parent
FAVICON = (SITE / "index.html").read_text().split('<link rel="icon" href="')[1].split('">')[0]

MONTH_UA = {7: "липня"}

# --- editorial calendar: slug -> (iso date, EN human, UA human) ---
CALENDAR = [
    ("what-is-llms-txt",            "2026-07-09"),
    ("check-ai-visibility",         "2026-07-10"),
    ("why-ai-recommends-competitors","2026-07-12"),
    ("geo-vs-seo",                  "2026-07-13"),
    ("google-ai-overviews",         "2026-07-15"),
    ("we-audited-our-own-site",     "2026-07-16"),
    ("ai-crawlers-guide",           "2026-07-18"),
    ("schema-for-ai",               "2026-07-19"),
    ("write-content-ai-quotes",     "2026-07-21"),
]
DATES = dict(CALENDAR)

def human(iso, lang):
    y, m, d = map(int, iso.split("-"))
    if lang == "en":
        return f"{['January','February','March','April','May','June','July','August','September','October','November','December'][m-1]} {d}, {y}"
    return f"{d} {MONTH_UA[m]} {y}"

def read_minutes(body):
    return max(2, round(len(re.sub(r"<[^>]+>", " ", body).split()) / 200))

TITLES = {}  # slug -> {lang: (title, h1, desc)}

def article_html(slug, lang, title, h1, desc, body, related):
    iso = DATES[slug]
    base = "/blog/" if lang == "en" else "/ua/blog/"
    canon = f"https://mentio.agency{base}{slug}/"
    alt_en = f"https://mentio.agency/blog/{slug}/"
    alt_uk = f"https://mentio.agency/ua/blog/{slug}/"
    other = f"/ua/blog/{slug}/" if lang == "en" else f"/blog/{slug}/"
    home = "/" if lang == "en" else "/ua/"
    blog = "/blog/" if lang == "en" else "/ua/blog/"
    rt = f"{read_minutes(body)} min read" if lang == "en" else f"{read_minutes(body)} хв читання"
    back = "← Blog" if lang == "en" else "← Блог"
    nav_geo = "What is GEO" if lang == "en" else "Що таке GEO"
    nav_srv = "Services" if lang == "en" else "Послуги"
    nav_blog = "Blog" if lang == "en" else "Блог"
    nav_cta = "Free check" if lang == "en" else "Безкоштовна перевірка"
    lang_lbl = "UA" if lang == "en" else "EN"
    rel_head = "Read next" if lang == "en" else "Читайте також"
    cta = (f'''<div class="post-cta">
  <p><strong>Want to know how AI assistants see your website?</strong> Run the free check — we reply with a summary of what ChatGPT, Perplexity and Gemini currently say about your business.</p>
  <a class="btn btn-primary" href="/#check">Check my website for free</a>
</div>''' if lang == "en" else f'''<div class="post-cta">
  <p><strong>Хочете знати, як AI-асистенти бачать ваш сайт?</strong> Пройдіть безкоштовну перевірку — у відповідь підсумок того, що ChatGPT, Perplexity і Gemini зараз кажуть про ваш бізнес.</p>
  <a class="btn btn-primary" href="/ua/#check">Перевірити мій сайт безкоштовно</a>
</div>''')
    rel_items = "".join(
        f'''      <a class="blog-item" href="{base}{s}/">
        <h3>{TITLES[s][lang][1]}</h3>
        <p>{TITLES[s][lang][2]}</p>
      </a>\n''' for s in related)

    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": canon + "#article", "headline": h1, "description": desc,
             "inLanguage": "uk" if lang == "uk" else "en",
             "datePublished": iso, "dateModified": iso,
             "image": "https://mentio.agency/assets/og.png", "mainEntityOfPage": canon,
             "author": {"@id": "https://mentio.agency/#org"},
             "publisher": {"@id": "https://mentio.agency/#org"},
             "speakable": {"@type": "SpeakableSpecification", "cssSelector": ["h1", ".post-body p:first-of-type"]}},
            {"@type": "Organization", "@id": "https://mentio.agency/#org", "name": "Mentio",
             "url": "https://mentio.agency/", "email": "team@mentio.agency",
             "sameAs": ["https://www.linkedin.com/company/mentio-agency/", "https://github.com/motornyysasha/mentio-site"],
             "logo": {"@type": "ImageObject", "url": "https://mentio.agency/assets/logo.png", "width": 512, "height": 512}},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Mentio", "item": "https://mentio.agency" + home},
                {"@type": "ListItem", "position": 2, "name": nav_blog, "item": "https://mentio.agency" + blog},
                {"@type": "ListItem", "position": 3, "name": h1}]}]
    }, ensure_ascii=False, indent=1)

    return f'''<!DOCTYPE html>
<html lang="{'en' if lang == 'en' else 'uk'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canon}">
<link rel="alternate" hreflang="en" href="{alt_en}">
<link rel="alternate" hreflang="uk" href="{alt_uk}">
<link rel="alternate" hreflang="x-default" href="{alt_en}">
<meta property="og:type" content="article">
<meta property="og:url" content="{canon}">
<meta property="og:site_name" content="Mentio">
<meta property="og:title" content="{h1}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="https://mentio.agency/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://mentio.agency/assets/og.png">
<link rel="icon" href="{FAVICON}">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/style.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body>

<nav>
  <div class="wrap nav-inner">
    <a class="logo" href="{home}"><span class="logo-dot"></span>Mentio</a>
    <div class="nav-links">
      <a href="{home}#geo">{nav_geo}</a>
      <a href="{home}#services">{nav_srv}</a>
      <a class="nav-blog" href="{blog}">{nav_blog}</a>
      <a class="lang-select" style="text-decoration:none" href="{other}" lang="{'uk' if lang == 'en' else 'en'}">{lang_lbl}</a>
      <a class="nav-cta" href="{home}#check">{nav_cta}</a>
    </div>
  </div>
</nav>

<div class="wrap post-head">
  <p class="post-meta"><a href="{blog}" style="color:inherit;text-decoration:none">{back}</a> · Mentio · {human(iso, lang)} · {rt}</p>
  <h1 style="font-size:clamp(1.7rem,3.6vw,2.5rem);letter-spacing:-.02em;line-height:1.2">{h1}</h1>
</div>
<article class="post">
  <div class="wrap">
    <div class="post-body">
{body}
    </div>
{cta}
    <div style="margin-top:2.6rem;max-width:760px">
      <p class="kicker">{rel_head}</p>
      <div class="blog-list">
{rel_items}      </div>
    </div>
  </div>
</article>

<footer>
  <div class="wrap foot">
    <span>© 2026 Mentio · Generative Engine Optimization</span>
    <span><a href="mailto:team@mentio.agency">team@mentio.agency</a> · <a href="{home}">{'Home' if lang == 'en' else 'Головна'}</a> · <a href="{blog}">{nav_blog}</a> · <a href="/llms.txt">llms.txt</a></span>
  </div>
</footer>
<script src="/assets/site.js" defer></script>
<script data-goatcounter="https://mentio.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>
</body>
</html>'''
