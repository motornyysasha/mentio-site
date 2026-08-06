#!/usr/bin/env python3
"""
Добавляет 7 новых статей (EN+UA), продолжая редакционный календарь блога.

Даты заполняют разрыв с 23 июля по 6 августа с шагом 2–3 дня — так же,
как выглядят уже опубликованные девять статей.

Шаблон берётся из текущего состояния сайта, а не из старого add_posts.py:
author = #founder (не #org), byline со ссылкой на LinkedIn, актуальный sameAs.

Запуск из корня сайта:  python3 tools/add_posts_aug.py
После: python3 bump-assets.py && git add -A && git commit && git push
"""
import json
import pathlib
import re

SITE = pathlib.Path(__file__).resolve().parent.parent
FAVICON = (SITE / "index.html").read_text(encoding="utf-8").split('<link rel="icon" href="')[1].split('">')[0]

FOUNDER = "Oleksandr Motornyy"
FOUNDER_LI = "https://www.linkedin.com/in/oleksandr-motornyy-7b9473169/"
SAME_AS = [
    "https://www.linkedin.com/company/mentio-agency/",
    "https://x.com/MentioAgency",
    "https://www.crunchbase.com/organization/mentio-152c",
    "https://github.com/motornyysasha/mentio-site",
]

MONTH_EN = ["January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"]
MONTH_UA = {7: "липня", 8: "серпня"}

# ---------------------------------------------------------------- календарь

NEW = [
    ("geo-score-53-to-71",          "2026-07-23"),
    ("no-guaranteed-citations",     "2026-07-25"),
    ("brand-entity-for-ai",         "2026-07-28"),
    ("eeat-for-ai-search",          "2026-07-30"),
    ("how-ai-picks-sources",        "2026-08-02"),
    ("security-headers-and-ai",     "2026-08-04"),
    ("geo-checklist-before-paying", "2026-08-06"),
]
DATES = dict(NEW)


def human(iso, lang):
    y, m, d = map(int, iso.split("-"))
    return f"{MONTH_EN[m-1]} {d}, {y}" if lang == "en" else f"{d} {MONTH_UA[m]} {y}"


def read_minutes(body):
    return max(2, round(len(re.sub(r"<[^>]+>", " ", body).split()) / 200))


# ------------------------------------------------------------------ контент
# P[slug][lang] = (title, h1, desc, body)
P = {}

# ---------------------------------------------------------------- 1. 53→71
P["geo-score-53-to-71"] = {"en": (
 "From 53 to 71: what actually moved our own GEO score — Mentio Blog",
 "From 53 to 71: what actually moved our own GEO score",
 "Two weeks after publishing our own audit at 53/100, we re-ran it: 71/100. Here is the honest breakdown of which fixes moved the number, which did nothing, and what is still broken.",
 """<p><strong>On 8 July our own site scored 53 out of 100 on the GEO audit we sell. On 23 July the same audit returned 71.</strong> Below is what changed between those two numbers — including the work that produced no measurable movement at all.</p>

<p>We publish this for a simple reason: an agency that sells measurement should show its own measurements. The <a href="/blog/we-audited-our-own-site/">first audit is here</a> if you want the starting point.</p>

<h2>The two scores, side by side</h2>

<table>
<thead><tr><th>Category</th><th>8 July</th><th>23 July</th><th>Change</th></tr></thead>
<tbody>
<tr><td>AI platform readiness</td><td>60</td><td>75</td><td>+15</td></tr>
<tr><td>Content quality / E-E-A-T</td><td>72</td><td>90</td><td>+18</td></tr>
<tr><td>Technical foundation</td><td>55</td><td>60</td><td>+5</td></tr>
<tr><td>Structured data</td><td>70</td><td>85</td><td>+15</td></tr>
<tr><td>Brand authority</td><td>5</td><td>35</td><td>+30</td></tr>
<tr><td><strong>Composite</strong></td><td><strong>53</strong></td><td><strong>71</strong></td><td><strong>+18</strong></td></tr>
</tbody>
</table>

<h2>What moved the number most</h2>

<h3>1. Putting a human on the site (+18 on content)</h3>

<p>The single biggest content jump came from the least technical change. Every article was signed "Mentio". Now every article is signed by a named person, with a <code>Person</code> node in the structured data, linked by <code>@id</code> to the organisation as its founder.</p>

<p>Nothing else about the articles changed. Same words, same structure. The score moved because E-E-A-T is not a writing-quality metric — it is an accountability metric. An unsigned page has nobody standing behind it.</p>

<h3>2. Existing on more than one website (+30 on authority)</h3>

<p>Brand authority went from 5 to 35 purely by existing in places we did not control. A company page, a Crunchbase entry, a social profile — each one saying the same name, the same description, the same URL.</p>

<p>The number is still low, and it should be. Thirty-five out of a hundred is an honest score for a brand that is a few weeks old. This is the category that cannot be rushed.</p>

<h3>3. llms.txt, FAQ markup and language versions (+15 each)</h3>

<p>These are the standard technical wins and they behaved exactly as expected. A machine-readable summary of the site, question-and-answer markup that mirrors how people actually ask, and six language versions correctly cross-linked with <code>hreflang</code>.</p>

<h2>What produced almost nothing</h2>

<p><strong>Technical foundation moved five points.</strong> Five. We spent real time on it, and the reason it barely moved is worth knowing: our host could not send custom HTTP headers at all. No amount of on-page work fixes a limitation that lives one layer below your site. We solved it later, by putting a proxy in front — and that is a separate story with <a href="/blog/security-headers-and-ai/">its own trap</a>.</p>

<p><strong>Publishing more articles, on its own, moved nothing.</strong> Volume is not a ranking input for AI systems the way it sometimes is for classic search. Two of our articles are cited-shaped — specific, self-contained, answerable. The rest are fine and contribute nothing measurable yet.</p>

<h2>What is still broken</h2>

<p><strong>Zero reviews.</strong> No <code>AggregateRating</code>, no <code>Review</code> markup, because we have no real reviews to point at. We will not invent them: fabricated ratings get the markup stripped from search results, and for an agency selling trust that is the worst possible trade. This stays broken until real clients leave real feedback.</p>

<p><strong>No verified business listing.</strong> Partially a choice, partially a platform limitation for our location.</p>

<h2>The honest lesson</h2>

<p>On-page GEO is a sprint you control. Crawler access, structured data, llms.txt, content shape — a competent developer moves those in a week, and our numbers show it: four categories jumped double digits in fourteen days.</p>

<p>Off-page authority is a season you schedule. It went up thirty points and still sits at thirty-five, because it is built from other people's websites mentioning you, and you cannot deploy that on a Tuesday.</p>

<p>If someone tells you they can fix both in the same sprint, ask which one they are lying about.</p>"""
), "uk": (
 "Від 53 до 71: що насправді зрушило нашу власну GEO-оцінку — Блог Mentio",
 "Від 53 до 71: що насправді зрушило нашу власну GEO-оцінку",
 "Через два тижні після публікації власного аудиту з оцінкою 53/100 ми провели його знову: 71/100. Чесний розбір того, які виправлення зрушили цифру, які не дали нічого, і що досі зламано.",
 """<p><strong>8 липня наш власний сайт отримав 53 бали зі 100 за тим самим GEO-аудитом, який ми продаємо. 23 липня той самий аудит показав 71.</strong> Нижче — що змінилося між цими двома цифрами, включно з роботою, яка не дала жодного вимірюваного результату.</p>

<p>Публікуємо це з простої причини: агенція, яка продає вимірювання, має показувати власні вимірювання. <a href="/ua/blog/we-audited-our-own-site/">Перший аудит тут</a>, якщо потрібна точка відліку.</p>

<h2>Дві оцінки поруч</h2>

<table>
<thead><tr><th>Категорія</th><th>8 липня</th><th>23 липня</th><th>Зміна</th></tr></thead>
<tbody>
<tr><td>Готовність AI-платформ</td><td>60</td><td>75</td><td>+15</td></tr>
<tr><td>Якість контенту / E-E-A-T</td><td>72</td><td>90</td><td>+18</td></tr>
<tr><td>Технічна основа</td><td>55</td><td>60</td><td>+5</td></tr>
<tr><td>Структуровані дані</td><td>70</td><td>85</td><td>+15</td></tr>
<tr><td>Авторитетність бренду</td><td>5</td><td>35</td><td>+30</td></tr>
<tr><td><strong>Разом</strong></td><td><strong>53</strong></td><td><strong>71</strong></td><td><strong>+18</strong></td></tr>
</tbody>
</table>

<h2>Що зрушило цифру найбільше</h2>

<h3>1. Поява живої людини на сайті (+18 за контент)</h3>

<p>Найбільший стрибок у контенті дала найменш технічна зміна. Раніше кожна стаття була підписана «Mentio». Тепер кожна підписана конкретною людиною, з вузлом <code>Person</code> у структурованих даних, пов'язаним через <code>@id</code> з організацією як її засновник.</p>

<p>Більше в статтях не змінилося нічого. Ті самі слова, та сама структура. Оцінка зросла тому, що E-E-A-T — це не метрика якості письма, а метрика відповідальності. За непідписаною сторінкою не стоїть ніхто.</p>

<h3>2. Існування не лише на власному сайті (+30 за авторитетність)</h3>

<p>Авторитетність бренду зросла з 5 до 35 виключно завдяки присутності там, де ми нічого не контролюємо. Сторінка компанії, запис у бізнес-каталозі, соціальний профіль — кожен із однаковою назвою, однаковим описом, однаковим посиланням.</p>

<p>Цифра досі низька, і так і має бути. Тридцять п'ять зі ста — чесна оцінка для бренду, якому кілька тижнів. Це та категорія, яку неможливо прискорити.</p>

<h3>3. llms.txt, FAQ-розмітка і мовні версії (+15 кожен)</h3>

<p>Стандартні технічні перемоги, які спрацювали саме так, як очікувалося. Машиночитний опис сайту, розмітка «питання — відповідь», що повторює реальні формулювання людей, і шість мовних версій, коректно пов'язаних через <code>hreflang</code>.</p>

<h2>Що не дало майже нічого</h2>

<p><strong>Технічна основа зросла на п'ять балів.</strong> П'ять. Ми витратили на неї реальний час, і причина мізерного результату варта уваги: наш хостинг узагалі не вмів віддавати кастомні HTTP-заголовки. Жодна робота на сторінці не виправляє обмеження, яке живе шаром нижче. Пізніше ми це вирішили, поставивши проксі — і це окрема історія <a href="/ua/blog/security-headers-and-ai/">зі своєю пасткою</a>.</p>

<p><strong>Публікація більшої кількості статей сама по собі не дала нічого.</strong> Обсяг не є вхідним сигналом для AI-систем так, як це іноді працює в класичному пошуку. Дві наші статті мають «цитовану» форму — конкретні, самодостатні, з прямою відповіддю. Решта нормальні й поки що не додають нічого вимірюваного.</p>

<h2>Що досі зламано</h2>

<p><strong>Нуль відгуків.</strong> Ні <code>AggregateRating</code>, ні розмітки <code>Review</code>, бо немає реальних відгуків, на які можна послатися. Вигадувати не будемо: за фальшиві рейтинги розмітку прибирають із видачі, а для агенції, що продає довіру, це найгірший можливий обмін. Лишається зламаним, доки реальні клієнти не залишать реальні відгуки.</p>

<p><strong>Немає верифікованої картки бізнесу.</strong> Частково вибір, частково обмеження платформи для нашої локації.</p>

<h2>Чесний висновок</h2>

<p>On-page GEO — це спринт, який ви контролюєте. Доступ краулерів, структуровані дані, llms.txt, форма контенту — компетентний розробник зрушить це за тиждень, і наші цифри це показують: чотири категорії стрибнули на двозначні значення за чотирнадцять днів.</p>

<p>Off-page авторитетність — це сезон, який ви плануєте. Вона зросла на тридцять балів і досі стоїть на тридцяти п'яти, бо будується з чужих сайтів, які вас згадують, а це не розгортається у вівторок.</p>

<p>Якщо хтось каже, що виправить обидва за один спринт, — питайте, про який саме він бреше.</p>"""
)}

# ------------------------------------------------------- 2. no guarantees
P["no-guaranteed-citations"] = {"en": (
 "Why nobody can guarantee you a place in AI answers — Mentio Blog",
 "Why nobody can guarantee you a place in AI answers",
 "Agencies promising guaranteed AI citations are selling something they do not control. Here is exactly where the control ends, and what an honest guarantee looks like instead.",
 """<p><strong>If an agency guarantees your business will appear in ChatGPT's answers, they are guaranteeing the behaviour of a system they have no access to.</strong> Not influence over — access to. The distinction matters, and this article is about where exactly the line falls.</p>

<h2>What you actually control</h2>

<p>Your side of the transaction is real and substantial:</p>

<ul>
<li><strong>Whether AI crawlers can read your site at all.</strong> Binary, verifiable, entirely yours.</li>
<li><strong>Whether your facts are machine-readable.</strong> Structured data either parses or it does not.</li>
<li><strong>Whether your content is shaped like an answer.</strong> A self-contained paragraph that resolves a question can be lifted. A paragraph of positioning cannot.</li>
<li><strong>Whether your brand exists in more than one place.</strong> Independent sources saying the same thing.</li>
</ul>

<p>Every item on that list is inspectable. You can check each one yourself, today, and confirm whether it was done.</p>

<h2>Where your control ends</h2>

<p>Everything after retrieval belongs to the platform operator:</p>

<ul>
<li><strong>Which sources the model picks</strong> for a given question, from a pool of thousands of eligible pages.</li>
<li><strong>How often it re-crawls</strong> and when your changes register.</li>
<li><strong>Whether it cites visibly</strong> or absorbs your content without attribution.</li>
<li><strong>Whether the ranking logic changes next month.</strong> It will, and nobody outside will be told.</li>
</ul>

<p>These are not difficult problems that a clever agency has solved. They are decisions made inside companies that do not publish their retrieval logic and do not offer a placement product. There is no API for "put this brand in the answer". There is no ad slot. There is no relationship to leverage.</p>

<h2>How the guarantee usually works in practice</h2>

<p>The promise is rarely an outright lie. It is usually a definition trick. Watch for these:</p>

<p><strong>Guaranteeing a query nobody asks.</strong> "We got you cited for <em>best GEO agency in Krāslava for fintech startups</em>." Congratulations — a query with zero monthly volume, where you were the only eligible source.</p>

<p><strong>Guaranteeing a screenshot.</strong> AI answers are non-deterministic and personalised. The same question produces different sources for different users on different days. A screenshot proves the sentence existed once, for someone.</p>

<p><strong>Guaranteeing "visibility" without defining it.</strong> If the contract does not say what is measured, on which platforms, with which questions, and how often — the guarantee has no failure condition. A guarantee that cannot be failed is not a guarantee.</p>

<h2>What an honest commitment looks like</h2>

<p>We do not promise citations. What can be promised without lying:</p>

<ol>
<li><strong>A documented method.</strong> Every check named, every finding evidenced, so you can reproduce it or hand it to someone else.</li>
<li><strong>A verifiable fix list.</strong> Each item with its own verification step. Not "improve your structured data" but "add this block, then confirm it here".</li>
<li><strong>An honest measurement.</strong> The same test, run the same way, before and after. Including the categories that did not move — <a href="/blog/geo-score-53-to-71/">ours moved five points in one category and thirty in another</a>, and both numbers are in the report.</li>
</ol>

<p>That is the whole offer. Everything past that point is a forecast, and it should be labelled as one.</p>

<h2>The question to ask any GEO vendor</h2>

<p>One question separates method from theatre:</p>

<p><strong>"What happens if the guarantee fails?"</strong></p>

<p>An honest answer names a specific, measurable failure condition and a specific remedy. A dishonest one redefines success until failure becomes impossible. You will know which one you got within about ten seconds.</p>"""
), "uk": (
 "Чому ніхто не може гарантувати вам місце у відповідях AI — Блог Mentio",
 "Чому ніхто не може гарантувати вам місце у відповідях AI",
 "Агенції, що обіцяють гарантовані цитування в AI, продають те, що не контролюють. Ось де саме закінчується контроль і як натомість виглядає чесна гарантія.",
 """<p><strong>Якщо агенція гарантує, що ваш бізнес з'явиться у відповідях ChatGPT, вона гарантує поведінку системи, до якої не має доступу.</strong> Не впливу на неї — саме доступу. Різниця принципова, і ця стаття про те, де точно проходить межа.</p>

<h2>Що ви справді контролюєте</h2>

<p>Ваш бік угоди реальний і суттєвий:</p>

<ul>
<li><strong>Чи можуть AI-краулери взагалі прочитати ваш сайт.</strong> Бінарно, перевірювано, повністю ваше.</li>
<li><strong>Чи є ваші факти машиночитними.</strong> Структуровані дані або парсяться, або ні.</li>
<li><strong>Чи має ваш контент форму відповіді.</strong> Самодостатній абзац, який закриває питання, можна процитувати. Абзац позиціонування — ні.</li>
<li><strong>Чи існує ваш бренд більш ніж в одному місці.</strong> Незалежні джерела, що кажуть те саме.</li>
</ul>

<p>Кожен пункт цього списку можна перевірити. Ви здатні перевірити його самостійно, сьогодні, і підтвердити, чи справді роботу зроблено.</p>

<h2>Де ваш контроль закінчується</h2>

<p>Усе після вибірки належить оператору платформи:</p>

<ul>
<li><strong>Які джерела модель обере</strong> для конкретного питання з тисяч придатних сторінок.</li>
<li><strong>Як часто вона переобходить сайт</strong> і коли ваші зміни зареєструються.</li>
<li><strong>Чи процитує помітно</strong> — чи поглине ваш контент без атрибуції.</li>
<li><strong>Чи зміниться логіка ранжування наступного місяця.</strong> Зміниться, і ззовні про це не повідомлять.</li>
</ul>

<p>Це не складні задачі, які розв'язала кмітлива агенція. Це рішення, ухвалені всередині компаній, що не публікують свою логіку вибірки й не продають продукт «розміщення». Немає API «додати цей бренд у відповідь». Немає рекламного слота. Немає зв'язків, якими можна скористатися.</p>

<h2>Як гарантія працює на практиці</h2>

<p>Обіцянка рідко буває відвертою брехнею. Зазвичай це трюк із визначенням. Ознаки:</p>

<p><strong>Гарантія за запитом, якого ніхто не ставить.</strong> «Ми забезпечили цитування за запитом <em>найкраща GEO-агенція в Краславі для фінтех-стартапів</em>». Вітаємо — запит із нульовою частотністю, де ви були єдиним придатним джерелом.</p>

<p><strong>Гарантія скриншота.</strong> Відповіді AI недетерміновані й персоналізовані. Те саме питання дає різні джерела різним людям у різні дні. Скриншот доводить, що речення існувало одного разу, для когось.</p>

<p><strong>Гарантія «видимості» без визначення.</strong> Якщо в договорі не сказано, що вимірюється, на яких платформах, якими питаннями і як часто — у гарантії немає умови невиконання. Гарантія, яку неможливо порушити, не є гарантією.</p>

<h2>Як виглядає чесне зобов'язання</h2>

<p>Ми не обіцяємо цитувань. Ось що можна пообіцяти, не збрехавши:</p>

<ol>
<li><strong>Задокументований метод.</strong> Кожна перевірка названа, кожна знахідка підтверджена, щоб ви могли відтворити її або передати іншому.</li>
<li><strong>Перевірюваний список виправлень.</strong> Кожен пункт зі своїм кроком перевірки. Не «покращте структуровані дані», а «додайте цей блок, потім підтвердьте тут».</li>
<li><strong>Чесний вимір.</strong> Той самий тест, проведений так само, до і після. Разом із категоріями, що не зрушили — <a href="/ua/blog/geo-score-53-to-71/">у нас одна зросла на п'ять балів, інша на тридцять</a>, і обидві цифри є у звіті.</li>
</ol>

<p>Це вся пропозиція. Усе поза цією межею — прогноз, і його треба позначати саме так.</p>

<h2>Питання, яке варто поставити будь-якому GEO-підряднику</h2>

<p>Одне питання відділяє метод від театру:</p>

<p><strong>«Що станеться, якщо гарантія не спрацює?»</strong></p>

<p>Чесна відповідь називає конкретну вимірювану умову невиконання і конкретне відшкодування. Нечесна перевизначає успіх, доки провал не стане неможливим. Ви зрозумієте, яку саме отримали, секунд за десять.</p>"""
)}

# --------------------------------------------------------- 3. brand entity
P["brand-entity-for-ai"] = {"en": (
 "One website is not enough: how AI decides your brand is real — Mentio Blog",
 "One website is not enough: how AI decides your brand is real",
 "AI systems treat a brand that exists on one website as an unverified claim. What an entity is, why cross-referencing matters more than volume, and the consistency mistake that quietly splits you in two.",
 """<p><strong>Your website says you exist. To an AI system, that is a claim, not a fact.</strong> The difference between a claim and a fact is whether anyone else says the same thing — and that is the whole mechanic behind brand entity.</p>

<h2>What an entity actually is</h2>

<p>An entity is a thing a machine has decided is real and distinct: this company, that person, this product. Not a keyword — a node, with attributes and relationships to other nodes.</p>

<p>When an AI system is asked to recommend a service provider, it is not matching text. It is checking whether a confident entity exists behind the name. A brand that appears on exactly one website, describing itself, has provided one unverified source. That is not enough to be recommended with confidence — and being recommended <em>with confidence</em> is the entire game.</p>

<h2>Cross-referencing beats volume</h2>

<p>Here is the part that surprises people: five profiles that agree are worth more than fifty that drift.</p>

<p>The mechanism is confirmation, not accumulation. Each independent source repeating the same name, description and URL raises the model's confidence that the entity is real. Sources that contradict each other lower it — because now the system has to decide which version is true, and hedging is cheaper than guessing wrong.</p>

<p>We found this in our own numbers. Brand authority sat at 5/100 with a website and nothing else. Adding a handful of consistent profiles took it to 35. The jump came from existing elsewhere, not from posting more.</p>

<h2>The consistency mistake that splits you in two</h2>

<p>The most common self-inflicted wound in entity building is looking like two different companies.</p>

<p>It happens quietly. The website says the founder is based in one country; the business listing gives an address in another. The company page spells the name with a hyphen; the directory spells it without. One profile transliterates a name as <em>Oleksandr</em>, another as <em>Alexander</em>.</p>

<p>None of these are lies. All of them force a machine to decide whether it is looking at one entity or two — and when it cannot tell, it splits the confidence between both. You end up competing with yourself.</p>

<p><strong>Practical rule:</strong> pick one canonical version of every fact — legal name, spelling, location, description, URL — write it down once, and copy-paste it everywhere. Never retype from memory. Retyping is how drift begins.</p>

<h2>Which places are worth the effort</h2>

<p>Not all sources carry equal weight. In rough order of return:</p>

<ol>
<li><strong>Business directories in your sector.</strong> These are where AI systems go when asked for a list of providers, because the list already exists in structured form.</li>
<li><strong>Company databases.</strong> Machine-readable, heavily crawled, and they encode relationships — founder, category, founding year — not just text.</li>
<li><strong>A professional network page.</strong> Widely trusted as an identity anchor.</li>
<li><strong>Your own structured data.</strong> The <code>sameAs</code> property is how you tell machines "these profiles are me". Without it, the profiles exist but are not connected to you.</li>
</ol>

<p>That last point is the one most people miss. Creating profiles is half the work. Declaring them in your own markup is what turns a scattered set of pages into one entity.</p>

<h2>The part that takes time</h2>

<p>Everything above is a week of work. What follows is not.</p>

<p>The strongest entity signal is being mentioned by someone with no reason to flatter you: a comparison article you did not commission, a forum answer where someone recommends you unprompted, a client writing about their results. You cannot deploy those. You can only do work worth mentioning and then ask.</p>

<p>Which is the honest summary of brand authority in general: the technical half is fast and yours, and the half that actually convinces a machine belongs to other people.</p>"""
), "uk": (
 "Одного сайту недостатньо: як AI вирішує, що ваш бренд справжній — Блог Mentio",
 "Одного сайту недостатньо: як AI вирішує, що ваш бренд справжній",
 "AI-системи сприймають бренд, який існує на одному сайті, як непідтверджену заяву. Що таке сутність, чому перехресне підтвердження важливіше за обсяг і яка помилка узгодженості тихо роздвоює вас.",
 """<p><strong>Ваш сайт стверджує, що ви існуєте. Для AI-системи це заява, а не факт.</strong> Різниця між заявою і фактом полягає в тому, чи каже те саме хтось іще — і саме на цьому побудована вся механіка сутності бренду.</p>

<h2>Що таке сутність насправді</h2>

<p>Сутність — це те, що машина визнала реальним і відокремленим: ця компанія, ця людина, цей продукт. Не ключове слово, а вузол з атрибутами і зв'язками з іншими вузлами.</p>

<p>Коли AI-систему просять порекомендувати виконавця, вона не зіставляє текст. Вона перевіряє, чи стоїть за назвою впевнена сутність. Бренд, присутній рівно на одному сайті, де він описує сам себе, надав одне непідтверджене джерело. Цього замало, щоб бути рекомендованим <em>упевнено</em>, — а саме впевненість тут і вирішує.</p>

<h2>Перехресне підтвердження важливіше за обсяг</h2>

<p>Ось що зазвичай дивує: п'ять профілів, які узгоджуються, коштують більше, ніж п'ятдесят, що розходяться.</p>

<p>Механізм — підтвердження, а не накопичення. Кожне незалежне джерело, що повторює ту саму назву, опис і посилання, підвищує впевненість моделі в реальності сутності. Джерела, які суперечать одне одному, знижують її — бо тепер системі треба вирішити, яка версія правдива, а обережність дешевша за помилку.</p>

<p>Ми побачили це на власних цифрах. Авторитетність бренду стояла на 5/100 із сайтом і нічим більше. Кілька узгоджених профілів підняли її до 35. Стрибок дала присутність деінде, а не більша кількість публікацій.</p>

<h2>Помилка узгодженості, яка роздвоює вас</h2>

<p>Найпоширеніша самозавдана шкода у побудові сутності — виглядати як дві різні компанії.</p>

<p>Це стається тихо. На сайті засновник в одній країні; у бізнес-картці адреса в іншій. На сторінці компанії назва з дефісом; у каталозі — без. В одному профілі ім'я транслітеровано як <em>Oleksandr</em>, в іншому — як <em>Alexander</em>.</p>

<p>Жодне з цього не є брехнею. Але кожне змушує машину вирішувати, чи бачить вона одну сутність, чи дві, — а коли розрізнити неможливо, впевненість ділиться між обома. Ви починаєте конкурувати самі з собою.</p>

<p><strong>Практичне правило:</strong> оберіть одну канонічну версію кожного факту — юридичну назву, написання, локацію, опис, посилання — запишіть її один раз і копіюйте всюди. Ніколи не набирайте з пам'яті. Саме з повторного набору починається розходження.</p>

<h2>Які майданчики варті зусиль</h2>

<p>Не всі джерела мають однакову вагу. Приблизно за віддачею:</p>

<ol>
<li><strong>Галузеві каталоги виконавців.</strong> Саме туди AI-системи йдуть за списком підрядників, бо список уже існує у структурованому вигляді.</li>
<li><strong>Бази компаній.</strong> Машиночитні, активно обходяться краулерами і кодують зв'язки — засновник, категорія, рік заснування, — а не лише текст.</li>
<li><strong>Сторінка у професійній мережі.</strong> Широко визнаний якір ідентичності.</li>
<li><strong>Ваші власні структуровані дані.</strong> Властивість <code>sameAs</code> — це спосіб сказати машинам «ці профілі — це я». Без неї профілі існують, але не пов'язані з вами.</li>
</ol>

<p>Останній пункт пропускають найчастіше. Створити профілі — половина роботи. Оголосити їх у власній розмітці — це те, що перетворює розкидані сторінки на одну сутність.</p>

<h2>Частина, яка потребує часу</h2>

<p>Усе вище — тиждень роботи. Те, що далі, — ні.</p>

<p>Найсильніший сигнал сутності — згадка від того, у кого немає причин вам лестити: порівняльна стаття, яку ви не замовляли, відповідь на форумі, де вас радять без прохання, клієнт, що пише про свої результати. Це не розгортається деплоєм. Можна лише робити роботу, варту згадки, а потім попросити.</p>

<p>Що і є чесним підсумком авторитетності загалом: технічна половина швидка і ваша, а половина, яка справді переконує машину, належить іншим людям.</p>"""
)}

# ------------------------------------------------------------- 4. E-E-A-T
P["eeat-for-ai-search"] = {"en": (
 "The cost of being anonymous: E-E-A-T in AI search — Mentio Blog",
 "The cost of being anonymous: E-E-A-T in AI search",
 "Unsigned content is treated as lower-confidence by AI systems. What each letter of E-E-A-T means in practice, why the first E is the hardest to fake, and the minimum viable authorship setup.",
 """<p><strong>We changed nothing about our articles except who signed them, and the content score moved eighteen points.</strong> Same sentences, same structure, same evidence. The only difference was a name, a role, and a link to a real profile.</p>

<p>That is the cheapest lesson in this article, so it goes first. What follows is why it works.</p>

<h2>The four letters, without the SEO fog</h2>

<p>E-E-A-T is Experience, Expertise, Authoritativeness, Trustworthiness. In practice they answer four different questions, and most sites only try to answer one.</p>

<p><strong>Experience — have you actually done this?</strong> Not studied it. Done it. First-hand contact with the thing you are describing. This is the newest addition to the framework and the hardest to manufacture, because it shows up in specifics: numbers you could only have if you ran the process, failures you would not invent, details nobody quotes from a competitor's blog.</p>

<p><strong>Expertise — do you know the subject?</strong> Demonstrated by accuracy and depth, undermined by vagueness. A page that hedges every claim reads as someone who has read about the topic rather than worked in it.</p>

<p><strong>Authoritativeness — does anyone else say you know it?</strong> This one is not on your website. It lives in other people's citations, mentions and links.</p>

<p><strong>Trustworthiness — is there a reason to believe you?</strong> Contact details that resolve, claims that are checkable, and someone accountable for what is written.</p>

<h2>Why anonymity costs more in AI search than in classic search</h2>

<p>Classic search ranks a list. A user who lands on an anonymous page can evaluate it themselves — look at the design, check the About page, decide.</p>

<p>An AI answer removes that step. The system quotes a claim and stands behind it. If the claim turns out to be wrong, the platform absorbs the reputational damage, not you. So the calculation shifts: given two pages with equivalent content, the one with an accountable author is a lower-risk source to repeat.</p>

<p>You are not being judged on writing quality. You are being judged on whether someone can be pointed at.</p>

<h2>The minimum viable setup</h2>

<p>This is genuinely small. Four things:</p>

<ol>
<li><strong>A real name on every article,</strong> visible in the byline, not buried in a footer.</li>
<li><strong>A <code>Person</code> node in your structured data,</strong> with a stable <code>@id</code>, linked as the article's <code>author</code> and as the organisation's <code>founder</code> or employee.</li>
<li><strong>A link from that person to an external profile</strong> that confirms they exist and do this work.</li>
<li><strong>A short, honest bio</strong> — real background, no invented credentials. See below.</li>
</ol>

<p>That is a couple of hours of work and it is the highest-return trust change available to a small site, because everything else in the trust layer depends on other people.</p>

<h2>Do not invent the biography</h2>

<p>The temptation with the first E is to inflate it. Resist, for two reasons.</p>

<p>The practical one: invented credentials are checkable. An AI system that cross-references your claimed background against external profiles and finds nothing has learned something about your reliability — and it is not what you hoped.</p>

<p>The strategic one: an honest unusual background is more persuasive than a generic impressive one. "Ten years in digital marketing" is unfalsifiable and forgettable. A specific, verifiable path — even a sideways one — gives a reason to trust the method rather than the title.</p>

<h2>What to do this week</h2>

<p>Open any article on your site. If it is signed by your company rather than a person, you are leaving the cheapest trust signal on the table.</p>

<p>Add the name. Add the <code>Person</code> markup. Link it to a profile that exists. Then move on to the parts that take months — <a href="/blog/brand-entity-for-ai/">the ones that depend on other people mentioning you</a>.</p>"""
), "uk": (
 "Ціна анонімності: E-E-A-T у пошуку з AI — Блог Mentio",
 "Ціна анонімності: E-E-A-T у пошуку з AI",
 "Непідписаний контент AI-системи вважають менш надійним. Що означає кожна літера E-E-A-T на практиці, чому перше E найважче підробити і який мінімальний набір авторства потрібен.",
 """<p><strong>Ми не змінили у статтях нічого, крім того, хто їх підписав, — і оцінка контенту зросла на вісімнадцять балів.</strong> Ті самі речення, та сама структура, ті самі докази. Різниця лише в імені, посаді та посиланні на реальний профіль.</p>

<p>Це найдешевший урок статті, тому він іде першим. Далі — чому це працює.</p>

<h2>Чотири літери без SEO-туману</h2>

<p>E-E-A-T — це Experience, Expertise, Authoritativeness, Trustworthiness: досвід, експертиза, авторитетність, довіра. На практиці вони відповідають на чотири різні питання, а більшість сайтів намагається відповісти лише на одне.</p>

<p><strong>Досвід — ви це справді робили?</strong> Не вивчали. Робили. Безпосередній контакт із тим, що описуєте. Це найновіший елемент моделі й найважчий для підробки, бо він проявляється в конкретиці: цифри, які можна мати лише пройшовши процес, невдачі, які не вигадують, деталі, яких не процитуєш із блогу конкурента.</p>

<p><strong>Експертиза — ви знаєте предмет?</strong> Демонструється точністю і глибиною, руйнується розмитістю. Сторінка, що обережно обходить кожне твердження, читається як текст того, хто про тему читав, а не працював у ній.</p>

<p><strong>Авторитетність — хтось іще каже, що ви це знаєте?</strong> Цього немає на вашому сайті. Воно живе в чужих цитуваннях, згадках і посиланнях.</p>

<p><strong>Довіра — чи є підстава вам вірити?</strong> Контакти, які працюють, твердження, які можна перевірити, і хтось, хто відповідає за написане.</p>

<h2>Чому анонімність коштує дорожче в AI-пошуку</h2>

<p>Класичний пошук ранжує список. Користувач, що потрапив на анонімну сторінку, оцінює її сам — дивиться на дизайн, заходить у розділ «про нас», вирішує.</p>

<p>Відповідь AI прибирає цей крок. Система цитує твердження і ручається за нього. Якщо твердження виявиться хибним, репутаційний удар приймає платформа, а не ви. Тож розрахунок змінюється: за двох сторінок з рівноцінним змістом та, у якої є відповідальний автор, — джерело з меншим ризиком.</p>

<p>Вас оцінюють не за якість письма. Вас оцінюють за те, чи є на кого вказати.</p>

<h2>Мінімальний робочий набір</h2>

<p>Він справді невеликий. Чотири речі:</p>

<ol>
<li><strong>Справжнє ім'я в кожній статті,</strong> видиме в підписі, а не заховане в підвалі.</li>
<li><strong>Вузол <code>Person</code> у структурованих даних</strong> зі стабільним <code>@id</code>, пов'язаний як <code>author</code> статті і як <code>founder</code> чи співробітник організації.</li>
<li><strong>Посилання від цієї людини на зовнішній профіль,</strong> що підтверджує: вона існує і займається цією роботою.</li>
<li><strong>Коротка чесна біографія</strong> — реальний бекграунд, без вигаданих регалій. Про це нижче.</li>
</ol>

<p>Це кілька годин роботи і найвигідніша зміна в шарі довіри для невеликого сайту, бо все інше в цьому шарі залежить від інших людей.</p>

<h2>Не вигадуйте біографію</h2>

<p>Спокуса з першим E — прикрасити. Не варто, з двох причин.</p>

<p>Практична: вигадані регалії перевіряються. AI-система, що звіряє заявлений бекграунд із зовнішніми профілями і не знаходить нічого, дізнається щось про вашу надійність — і не те, на що ви сподівалися.</p>

<p>Стратегічна: чесний незвичний шлях переконує сильніше за загальний вражаючий. «Десять років у діджитал-маркетингу» — нефальсифіковано і забувається одразу. Конкретний перевірюваний шлях, навіть збоку, дає підставу довіряти методу, а не титулу.</p>

<h2>Що зробити цього тижня</h2>

<p>Відкрийте будь-яку статтю на своєму сайті. Якщо вона підписана компанією, а не людиною, ви залишаєте найдешевший сигнал довіри невикористаним.</p>

<p>Додайте ім'я. Додайте розмітку <code>Person</code>. Зв'яжіть її з профілем, який існує. А потім переходьте до того, що займає місяці, — <a href="/ua/blog/brand-entity-for-ai/">до речей, які залежать від згадок іншими людьми</a>.</p>"""
)}

# ------------------------------------------------------- 5. how AI picks
P["how-ai-picks-sources"] = {"en": (
 "How ChatGPT, Perplexity and Gemini each pick their sources — Mentio Blog",
 "How ChatGPT, Perplexity and Gemini each pick their sources",
 "The major AI assistants retrieve differently, and optimising for one does not automatically win the others. What each system favours, and the work that pays off across all of them.",
 """<p><strong>The same question, asked of three AI assistants, will often produce three different sets of sources.</strong> Not because one is right and the others wrong, but because they retrieve differently. Knowing how each behaves tells you where your effort actually lands.</p>

<p>One caveat before the detail: none of these companies publish their retrieval logic, and all of them change it. What follows is drawn from observed behaviour, not documentation. Treat it as a working model, not a specification.</p>

<h2>Perplexity — search-first, citation-heavy</h2>

<p>Perplexity behaves most like a search engine with a writer attached. It retrieves live results for nearly every query and cites visibly, with numbered sources next to the claims.</p>

<p><strong>What it favours:</strong> pages that answer the specific question directly, recency, and clean extractable structure. Because citations are shown, there is a visible payoff for being quotable rather than merely relevant.</p>

<p><strong>What this means for you:</strong> this is the platform where <a href="/blog/write-content-ai-quotes/">content shape matters most</a>. A self-contained paragraph that resolves a question outperforms a longer page that circles it. It is also the fastest platform to reflect changes — useful when you want to measure whether a fix worked.</p>

<h2>ChatGPT — mixed retrieval, brand-weighted</h2>

<p>ChatGPT answers some questions from training and others by searching live, and the boundary is not announced to the user. For anything time-sensitive or specific it retrieves; for general knowledge it often does not.</p>

<p><strong>What it favours:</strong> when it retrieves, established sources and clear entity signals. When it does not retrieve, whatever was consolidated during training — which is where brand mentions across many independent sites pay off, because that is what made it into the model in the first place.</p>

<p><strong>What this means for you:</strong> two separate jobs. Crawler access and page structure serve the retrieval path. <a href="/blog/brand-entity-for-ai/">Entity building across external sites</a> serves the other one. Neither substitutes for the other.</p>

<h2>Google AI Overviews — the classic index, distilled</h2>

<p>AI Overviews sit on top of Google's existing index and infrastructure. If you are invisible in Google's index, you are invisible here.</p>

<p><strong>What it favours:</strong> everything classic SEO already favours — crawlability, structured data, topical depth, site quality signals — plus a strong preference for content that maps cleanly onto a question.</p>

<p><strong>What this means for you:</strong> this is the platform where GEO and SEO overlap most. Structured data does real work here. So does having your facts stated as facts rather than implied by marketing copy.</p>

<h2>Gemini — knowledge-graph leaning</h2>

<p>Gemini draws heavily on Google's entity understanding. It tends to be conservative about recommending things it cannot confirm exist as distinct entities.</p>

<p><strong>What it favours:</strong> confirmed entities with consistent attributes across sources. This is the platform where the <a href="/blog/brand-entity-for-ai/">consistency problem</a> hurts most — contradictory data about your business is worse here than almost anywhere.</p>

<h2>Bing Copilot — index freshness matters</h2>

<p>Copilot runs on Bing's index, which most sites neglect entirely. That neglect is an opportunity: the competitive field is thinner.</p>

<p><strong>What this means for you:</strong> submit your site to Bing's webmaster tools and use the instant-indexing protocol so new pages register in hours rather than weeks. It is a small task most competitors skip.</p>

<h2>The work that pays across all five</h2>

<p>Chasing each platform separately is a poor use of time. Four things pay off everywhere:</p>

<ol>
<li><strong>Let the crawlers in.</strong> Nothing else matters if this is wrong, and it is wrong more often than people expect.</li>
<li><strong>State facts in machine-readable form.</strong> Structured data is read by every system here.</li>
<li><strong>Shape content as answers.</strong> Helps retrieval-based systems directly and everything else indirectly.</li>
<li><strong>Be consistently described in several places.</strong> Helps entity-based systems directly and retrieval-based systems as a quality signal.</li>
</ol>

<p>Platform-specific tuning is worth doing after those four are solid — and not before.</p>"""
), "uk": (
 "Як ChatGPT, Perplexity і Gemini обирають свої джерела — Блог Mentio",
 "Як ChatGPT, Perplexity і Gemini обирають свої джерела",
 "Основні AI-асистенти працюють із джерелами по-різному, і оптимізація під один не виграє автоматично інші. Що цінує кожна система і яка робота окупається всюди.",
 """<p><strong>Те саме питання, поставлене трьом AI-асистентам, часто дає три різні набори джерел.</strong> Не тому, що один правий, а інші ні, — а тому, що вони по-різному шукають. Розуміння цієї різниці показує, куди насправді потрапляють ваші зусилля.</p>

<p>Одне застереження перед деталями: жодна з цих компаній не публікує логіку вибірки, і всі її змінюють. Нижче — узагальнення спостережуваної поведінки, а не документація. Сприймайте як робочу модель, не як специфікацію.</p>

<h2>Perplexity — спершу пошук, багато цитат</h2>

<p>Perplexity поводиться найбільше як пошуковик із приставленим редактором. Він шукає в реальному часі майже на кожен запит і цитує помітно, з пронумерованими джерелами поруч із твердженнями.</p>

<p><strong>Що цінує:</strong> сторінки, які прямо відповідають на конкретне питання, свіжість і чисту структуру, з якої легко витягти фрагмент. Оскільки цитати показуються, є видима винагорода за «цитовану» форму, а не просто за релевантність.</p>

<p><strong>Що це означає для вас:</strong> саме тут <a href="/ua/blog/write-content-ai-quotes/">форма контенту важить найбільше</a>. Самодостатній абзац, що закриває питання, виграє в довшої сторінки, яка ходить навколо. Це також найшвидша платформа з погляду відображення змін — зручно, коли треба перевірити, чи спрацювало виправлення.</p>

<h2>ChatGPT — змішана вибірка, вага бренду</h2>

<p>ChatGPT відповідає на одні питання з навчання, на інші — шукаючи наживо, і межу користувачеві не повідомляють. Для чутливого до часу чи конкретного він шукає; для загального знання часто ні.</p>

<p><strong>Що цінує:</strong> коли шукає — усталені джерела й чіткі сигнали сутності. Коли не шукає — те, що закріпилося під час навчання, а це саме там окупаються згадки бренду на багатьох незалежних сайтах, бо саме вони туди й потрапили.</p>

<p><strong>Що це означає для вас:</strong> дві окремі задачі. Доступ краулерів і структура сторінки обслуговують шлях із пошуком. <a href="/ua/blog/brand-entity-for-ai/">Побудова сутності на зовнішніх сайтах</a> обслуговує інший. Одне не замінює друге.</p>

<h2>Google AI Overviews — класичний індекс, стиснутий</h2>

<p>AI Overviews стоять поверх наявного індексу та інфраструктури Google. Якщо вас не видно в індексі Google, вас не видно й тут.</p>

<p><strong>Що цінує:</strong> усе, що вже цінує класичне SEO — обхід, структуровані дані, тематичну глибину, сигнали якості сайту — плюс виражену перевагу контенту, який чітко лягає на питання.</p>

<p><strong>Що це означає для вас:</strong> саме тут GEO і SEO перетинаються найбільше. Структуровані дані виконують реальну роботу. Як і формулювання фактів фактами, а не натяками в маркетинговому тексті.</p>

<h2>Gemini — з опорою на граф знань</h2>

<p>Gemini значною мірою спирається на розуміння сутностей у Google. Він схильний бути обережним із рекомендаціями того, чиє існування як окремої сутності підтвердити не вдається.</p>

<p><strong>Що цінує:</strong> підтверджені сутності з узгодженими атрибутами в різних джерелах. Саме тут <a href="/ua/blog/brand-entity-for-ai/">проблема неузгодженості</a> б'є найболючіше — суперечливі дані про ваш бізнес шкодять тут сильніше, ніж майже будь-де.</p>

<h2>Bing Copilot — свіжість індексу</h2>

<p>Copilot працює на індексі Bing, який більшість сайтів ігнорує повністю. Це ігнорування — можливість: конкурентне поле тут рідше.</p>

<p><strong>Що це означає для вас:</strong> додайте сайт до інструментів для вебмайстрів Bing і використовуйте протокол миттєвої індексації, щоб нові сторінки реєструвалися за години, а не за тижні. Невелика задача, яку більшість конкурентів пропускає.</p>

<h2>Робота, що окупається на всіх п'яти</h2>

<p>Ганятися за кожною платформою окремо — погане використання часу. Чотири речі працюють усюди:</p>

<ol>
<li><strong>Впустіть краулерів.</strong> Якщо тут помилка, решта не має значення, а помиляються тут частіше, ніж здається.</li>
<li><strong>Викладіть факти машиночитно.</strong> Структуровані дані читає кожна система зі списку.</li>
<li><strong>Надайте контенту форму відповіді.</strong> Прямо допомагає системам із пошуком і опосередковано — решті.</li>
<li><strong>Будьте узгоджено описані в кількох місцях.</strong> Прямо допомагає системам на сутностях і працює як сигнал якості для решти.</li>
</ol>

<p>Тонке налаштування під конкретну платформу варте зусиль після того, як ці чотири зроблено, — і не раніше.</p>"""
)}

# ------------------------------------------------ 6. security headers + AI
P["security-headers-and-ai"] = {"en": (
 "Security headers without breaking AI visibility — Mentio Blog",
 "Security headers without breaking AI visibility",
 "Adding a CDN proxy for security headers can silently block AI crawlers and break your own site. The two traps we hit doing it on mentio.agency, and how to avoid both.",
 """<p><strong>Adding security headers to our own site broke the language switcher and nearly blocked every AI crawler we spend our working life trying to attract.</strong> Both problems were self-inflicted, both were silent, and both are easy to repeat. Here is the full account.</p>

<h2>Why this comes up at all</h2>

<p>Technical audits check for a handful of HTTP response headers: a content security policy, <code>X-Content-Type-Options</code>, <code>Strict-Transport-Security</code>, <code>Referrer-Policy</code>. Their direct effect on AI visibility is modest, but they appear on every technical quality checklist, and some static hosts cannot send custom headers at all.</p>

<p>The standard fix is to put a CDN proxy in front of the host and add the headers there. That works. It also introduces two traps.</p>

<h2>Trap one: the proxy offers to block AI crawlers, and the default is yes</h2>

<p>During setup, our CDN offered a panel of AI bot controls: search crawlers, agent crawlers, training crawlers. The recommended default for training crawlers was <strong>block</strong>, with an additional toggle — enabled by default — to write those blocks into <code>robots.txt</code> automatically.</p>

<p>Think about what that means. Our <code>robots.txt</code> explicitly welcomes every AI crawler. Our blog argues that businesses should let them in. And the infrastructure layer was one click away from overriding all of it, silently, by rewriting the file.</p>

<p>For a publisher protecting original work, blocking training crawlers is a defensible position. For any business that wants to be found and recommended by AI assistants, it is self-sabotage — and it happens at a layer most people never re-check after setup.</p>

<p><strong>What to do:</strong> after any CDN or security change, re-fetch your own <code>robots.txt</code> over the public internet and read it. Not the file in your repository — the one your domain actually serves. They can differ, and the difference is invisible from your editor.</p>

<h2>Trap two: a strict CSP kills inline event handlers</h2>

<p>We set a deliberately strict content security policy: <code>script-src 'self'</code> plus one analytics domain, with no <code>'unsafe-inline'</code>. We checked the site for inline <code>&lt;script&gt;</code> blocks, found none, and shipped it.</p>

<p>Two weeks later the language switcher stopped working.</p>

<p>The switcher was a <code>&lt;select onchange="location.href=this.value"&gt;</code>. An inline event handler attribute is inline script, and the same directive blocks it. It does not error loudly. The handler simply never registers — the console stays clean, the element looks fine in the inspector, and nothing happens on interaction.</p>

<p>The failure was also delayed. The code had not changed in weeks; it broke the moment the headers went live. Nothing in the deployment log pointed at the cause.</p>

<p><strong>The fix, and the wrong fix.</strong> The tempting repair is adding <code>'unsafe-inline'</code> to <code>script-src</code>. One line, everything works, and you have just cancelled the main benefit of the policy you installed.</p>

<p>The correct repair is to move the handler into your existing script file:</p>

<pre><code>document.querySelectorAll("select.lang-select").forEach(function (sel) {
  sel.addEventListener("change", function () {
    if (this.value) location.href = this.value;
  });
});</code></pre>

<p>Policy stays strict, feature works. Inline <code>style</code> attributes are unaffected — <code>style-src</code> is a separate directive and can keep <code>'unsafe-inline'</code> without weakening script protection.</p>

<h2>Writing a CSP that does not break your own site</h2>

<p>A policy copied from a checklist will block something you depend on. Ours had to allow three external origins: the analytics script, the endpoint it reports to, and the form-handling worker. A generic <code>default-src 'self'</code> would have silently killed both analytics and lead capture.</p>

<p>Practical sequence:</p>

<ol>
<li><strong>Inventory what your pages actually load.</strong> Scripts, fonts, images, and every endpoint your JavaScript calls.</li>
<li><strong>Grep for <code>on*=</code> attributes</strong> across your templates. Every one is about to stop working.</li>
<li><strong>Deploy, then click through the live site with the console open.</strong> Every violation prints a directive name — that name tells you exactly what to add.</li>
<li><strong>Test the things that submit,</strong> not just the things that render. Forms fail differently from layouts.</li>
</ol>

<h2>The general lesson</h2>

<p>Infrastructure changes are invisible in your codebase. Nothing in the repository records that headers were added, so when something breaks two weeks later, the cause is not where anyone will look.</p>

<p>After any change at that layer, verify three things from the public internet: your <code>robots.txt</code> reads as intended, your response headers are what you set, and your interactive elements still work. Ten minutes, and it catches exactly the class of failure that otherwise goes unnoticed for months.</p>"""
), "uk": (
 "Security-заголовки без втрати видимості в AI — Блог Mentio",
 "Security-заголовки без втрати видимості в AI",
 "Додавання CDN-проксі заради security-заголовків може тихо заблокувати AI-краулерів і зламати ваш власний сайт. Дві пастки, в які ми потрапили на mentio.agency, і як обійти обидві.",
 """<p><strong>Додавання security-заголовків на власний сайт зламало перемикач мов і мало не заблокувало всіх AI-краулерів, яких ми професійно намагаємося привабити.</strong> Обидві проблеми ми створили собі самі, обидві були беззвучні, обидві легко повторити. Ось повний звіт.</p>

<h2>Чому це взагалі виникає</h2>

<p>Технічні аудити перевіряють кілька HTTP-заголовків відповіді: політику безпеки контенту, <code>X-Content-Type-Options</code>, <code>Strict-Transport-Security</code>, <code>Referrer-Policy</code>. Їхній прямий вплив на видимість в AI помірний, але вони є в кожному чеклисті технічної якості, а деякі статичні хостинги не вміють віддавати кастомні заголовки взагалі.</p>

<p>Стандартне рішення — поставити CDN-проксі перед хостингом і додати заголовки там. Це працює. І це відкриває дві пастки.</p>

<h2>Пастка перша: проксі пропонує заблокувати AI-краулерів, і за замовчуванням — так</h2>

<p>Під час налаштування наш CDN показав панель керування AI-ботами: пошукові краулери, агентські, тренувальні. Рекомендованим значенням для тренувальних було <strong>блокувати</strong>, з додатковим перемикачем — увімкненим за замовчуванням, — який автоматично вписує ці заборони в <code>robots.txt</code>.</p>

<p>Вдумайтеся. Наш <code>robots.txt</code> явно вітає кожного AI-краулера. Наш блог доводить, що бізнесу варто їх впускати. А інфраструктурний шар був за один клік від того, щоб перекреслити все це, тихо переписавши файл.</p>

<p>Для видавця, який захищає оригінальні матеріали, блокування тренувальних краулерів — позиція, яку можна відстоювати. Для будь-якого бізнесу, що хоче бути знайденим і рекомендованим AI-асистентами, це самосаботаж — і стається він на рівні, який після налаштування майже ніхто не переперевіряє.</p>

<p><strong>Що робити:</strong> після будь-якої зміни на CDN чи в безпеці запросіть власний <code>robots.txt</code> через публічний інтернет і прочитайте його. Не файл у репозиторії — той, який реально віддає ваш домен. Вони можуть відрізнятися, і з редактора цю різницю не видно.</p>

<h2>Пастка друга: суворий CSP вбиває inline-обробники подій</h2>

<p>Ми свідомо задали сувору політику безпеки контенту: <code>script-src 'self'</code> плюс один домен аналітики, без <code>'unsafe-inline'</code>. Перевірили сайт на inline-блоки <code>&lt;script&gt;</code>, не знайшли жодного і випустили.</p>

<p>За два тижні перемикач мов перестав працювати.</p>

<p>Перемикач був <code>&lt;select onchange="location.href=this.value"&gt;</code>. Атрибут-обробник події — це теж inline-скрипт, і та сама директива його блокує. Гучної помилки не буде. Обробник просто не реєструється: консоль чиста, елемент в інспекторі виглядає нормально, а на взаємодію нічого не відбувається.</p>

<p>Збій був ще й відкладеним. Код не змінювався тижнями; він зламався тієї миті, коли заголовки пішли в бій. У журналі деплою на причину не вказувало ніщо.</p>

<p><strong>Правильне і неправильне виправлення.</strong> Спокуслива поправка — додати <code>'unsafe-inline'</code> до <code>script-src</code>. Один рядок, усе працює, і ви щойно скасували головну користь від політики, яку встановлювали.</p>

<p>Правильна поправка — перенести обробник у наявний файл скрипта:</p>

<pre><code>document.querySelectorAll("select.lang-select").forEach(function (sel) {
  sel.addEventListener("change", function () {
    if (this.value) location.href = this.value;
  });
});</code></pre>

<p>Політика лишається суворою, функція працює. Inline-атрибути <code>style</code> не постраждали — <code>style-src</code> це окрема директива, і вона може зберігати <code>'unsafe-inline'</code>, не послаблюючи захист скриптів.</p>

<h2>Як написати CSP, що не ламає ваш сайт</h2>

<p>Політика, скопійована з чеклиста, заблокує щось потрібне. Наша мала пропустити три зовнішні джерела: скрипт аналітики, точку, куди він надсилає дані, і воркер, що приймає заявки з форм. Узагальнений <code>default-src 'self'</code> тихо вбив би і аналітику, і збір лідів.</p>

<p>Практична послідовність:</p>

<ol>
<li><strong>Складіть перелік того, що сторінки реально завантажують.</strong> Скрипти, шрифти, зображення і кожну точку, до якої звертається ваш JavaScript.</li>
<li><strong>Прогрепайте шаблони на атрибути <code>on*=</code>.</strong> Кожен із них зараз перестане працювати.</li>
<li><strong>Задеплойте і проклікайте живий сайт із відкритою консоллю.</strong> Кожне порушення друкує назву директиви — вона й підкаже, що додати.</li>
<li><strong>Перевіряйте те, що надсилає,</strong> а не лише те, що відображається. Форми ламаються інакше, ніж макети.</li>
</ol>

<h2>Загальний висновок</h2>

<p>Зміни в інфраструктурі невидимі у вашій кодовій базі. Ніщо в репозиторії не фіксує, що додали заголовки, тож коли за два тижні щось ламається, причина лежить не там, де її шукатимуть.</p>

<p>Після будь-якої зміни на цьому рівні перевірте три речі з публічного інтернету: чи <code>robots.txt</code> читається як задумано, чи заголовки відповіді саме такі, як ви задали, і чи працюють інтерактивні елементи. Десять хвилин — і ви ловите саме той клас збоїв, який інакше залишається непоміченим місяцями.</p>"""
)}

# ---------------------------------------------------------- 7. checklist
P["geo-checklist-before-paying"] = {"en": (
 "12 checks to run before you pay anyone for GEO — Mentio Blog",
 "12 checks to run before you pay anyone for GEO",
 "Most of a GEO audit is verifiable by the site owner in under an hour. Run these twelve checks first — they tell you what you need, and whether the vendor quoting you knows their job.",
 """<p><strong>Most of what a GEO audit checks, you can verify yourself in under an hour, for free.</strong> Do it before you buy anything. You will learn what you actually need, and you will be able to tell within one conversation whether the person quoting you knows the subject.</p>

<p>No tools required beyond a browser.</p>

<h2>Access — can AI systems read you at all</h2>

<p><strong>1. Open <code>yourdomain.com/robots.txt</code>.</strong> Look for <code>Disallow</code> rules that apply to <code>*</code>, and for named AI bots: <code>GPTBot</code>, <code>ClaudeBot</code>, <code>PerplexityBot</code>, <code>OAI-SearchBot</code>, <code>Google-Extended</code>. If any are blocked, nothing downstream matters. <a href="/blog/ai-crawlers-guide/">Full crawler reference here.</a></p>

<p><strong>2. Check the file your domain serves, not the one in your repository.</strong> A CDN or security layer can rewrite it. <a href="/blog/security-headers-and-ai/">We nearly did this to ourselves.</a></p>

<p><strong>3. Disable JavaScript in your browser and reload your key pages.</strong> If the content vanishes, some crawlers see an empty page.</p>

<p><strong>4. View source on your homepage and search for <code>noindex</code>.</strong> It ends up in production more often than anyone admits.</p>

<h2>Machine-readable facts</h2>

<p><strong>5. Paste your homepage URL into a structured data validator.</strong> You are looking for an <code>Organization</code> node with name, URL and contact details. Errors here mean the markup exists but is not being read.</p>

<p><strong>6. Check whether your structured data names a person.</strong> An <code>author</code> that points at the company rather than a human is the cheapest trust signal left on the table. <a href="/blog/eeat-for-ai-search/">Why it matters.</a></p>

<p><strong>7. Look for <code>sameAs</code>.</strong> If your markup does not list your external profiles, machines have no way to connect them to you. <a href="/blog/brand-entity-for-ai/">Entity building explained.</a></p>

<p><strong>8. Open <code>yourdomain.com/llms.txt</code>.</strong> Optional, but its absence tells you nobody has done the AI-specific layer. <a href="/blog/what-is-llms-txt/">What it is.</a></p>

<h2>Content shape</h2>

<p><strong>9. Pick your most important page and find one paragraph that answers a customer question completely, on its own.</strong> If every paragraph needs the ones around it for context, there is nothing an assistant can lift. <a href="/blog/write-content-ai-quotes/">How to fix that.</a></p>

<p><strong>10. Search your own site for your prices, timelines and specifics.</strong> If the concrete facts a buyer needs are not written down as facts, an AI cannot repeat them.</p>

<h2>Reality check</h2>

<p><strong>11. Ask three assistants directly.</strong> "What do you know about [your brand]?" and "Who are the best [your category] providers in [your market]?" Note whether you appear, whether the details are right, and who appears instead. This takes five minutes and is the single most informative check on the list.</p>

<p><strong>12. Search your brand name and see what exists besides your own site.</strong> One result means an unverified claim. Several consistent ones mean a confirmed entity.</p>

<h2>Reading your results</h2>

<p>If checks 1–4 fail, you have an access problem. It is the cheapest thing to fix and the most damaging to leave.</p>

<p>If 1–4 pass and 5–8 fail, you have a legibility problem. Machines can reach you but cannot parse what you are.</p>

<p>If those pass and 11–12 are weak, you have an authority problem — the slow one. No technical work shortcuts it.</p>

<h2>Three questions for any vendor</h2>

<p>Once you know your own numbers, these separate method from theatre:</p>

<p><strong>"Which of these twelve did you check, and what did you find?"</strong> A real audit covers all of them and shows evidence.</p>

<p><strong>"What does the price include beyond the list of problems?"</strong> A diagnosis without a fix list is half a product.</p>

<p><strong>"What happens if it does not work?"</strong> <a href="/blog/no-guaranteed-citations/">Anyone guaranteeing citations is promising something they do not control.</a></p>

<p>If a vendor's findings match what you found yourself, and they explain the parts you could not check, they are worth paying. If their report is vaguer than your own hour of work, you already know more than they do.</p>"""
), "uk": (
 "12 перевірок, які варто зробити до того, як платити за GEO — Блог Mentio",
 "12 перевірок, які варто зробити до того, як платити за GEO",
 "Більшість GEO-аудиту власник сайту може перевірити сам менш ніж за годину. Зробіть ці дванадцять перевірок першими — вони покажуть, що вам потрібно, і чи розуміє підрядник свою справу.",
 """<p><strong>Більшість того, що перевіряє GEO-аудит, ви можете перевірити самі менш ніж за годину і безкоштовно.</strong> Зробіть це до того, як щось купувати. Ви зрозумієте, що вам справді потрібно, і за одну розмову визначите, чи розуміє предмет той, хто виставляє вам рахунок.</p>

<p>Жодних інструментів, крім браузера.</p>

<h2>Доступ — чи можуть AI-системи вас прочитати</h2>

<p><strong>1. Відкрийте <code>вашдомен.com/robots.txt</code>.</strong> Шукайте правила <code>Disallow</code> для <code>*</code> і згадки конкретних AI-ботів: <code>GPTBot</code>, <code>ClaudeBot</code>, <code>PerplexityBot</code>, <code>OAI-SearchBot</code>, <code>Google-Extended</code>. Якщо когось заблоковано, усе подальше не має значення. <a href="/ua/blog/ai-crawlers-guide/">Повний довідник по краулерах.</a></p>

<p><strong>2. Перевіряйте файл, який віддає ваш домен, а не той, що в репозиторії.</strong> CDN або шар безпеки може його переписати. <a href="/ua/blog/security-headers-and-ai/">Ми самі мало цього не зробили.</a></p>

<p><strong>3. Вимкніть JavaScript у браузері й перезавантажте ключові сторінки.</strong> Якщо контент зникає — частина краулерів бачить порожню сторінку.</p>

<p><strong>4. Подивіться код головної сторінки й пошукайте <code>noindex</code>.</strong> Він потрапляє в продакшн частіше, ніж хтось зізнається.</p>

<h2>Машиночитні факти</h2>

<p><strong>5. Вставте адресу головної у валідатор структурованих даних.</strong> Шукайте вузол <code>Organization</code> з назвою, посиланням і контактами. Помилки тут означають, що розмітка є, але не читається.</p>

<p><strong>6. Перевірте, чи названо в розмітці людину.</strong> <code>author</code>, який вказує на компанію замість людини, — найдешевший невикористаний сигнал довіри. <a href="/ua/blog/eeat-for-ai-search/">Чому це важливо.</a></p>

<p><strong>7. Пошукайте <code>sameAs</code>.</strong> Якщо ваша розмітка не перелічує зовнішні профілі, машини не можуть пов'язати їх із вами. <a href="/ua/blog/brand-entity-for-ai/">Про побудову сутності.</a></p>

<p><strong>8. Відкрийте <code>вашдомен.com/llms.txt</code>.</strong> Необов'язковий, але його відсутність каже, що AI-специфічним шаром ніхто не займався. <a href="/ua/blog/what-is-llms-txt/">Що це таке.</a></p>

<h2>Форма контенту</h2>

<p><strong>9. Візьміть найважливішу сторінку і знайдіть абзац, який повністю відповідає на питання клієнта сам по собі.</strong> Якщо кожен абзац потребує сусідніх для контексту, асистенту нічого взяти. <a href="/ua/blog/write-content-ai-quotes/">Як це виправити.</a></p>

<p><strong>10. Пошукайте на власному сайті свої ціни, терміни й конкретику.</strong> Якщо конкретні факти, потрібні покупцеві, не записані як факти, AI не зможе їх повторити.</p>

<h2>Перевірка реальністю</h2>

<p><strong>11. Запитайте трьох асистентів прямо.</strong> «Що ти знаєш про [ваш бренд]?» і «Хто найкращі [ваша категорія] у [ваш ринок]?» Занотуйте, чи з'являєтесь ви, чи правильні деталі й хто з'являється замість вас. П'ять хвилин — і це найінформативніша перевірка зі списку.</p>

<p><strong>12. Пошукайте назву свого бренду й подивіться, що існує, крім вашого сайту.</strong> Один результат — це непідтверджена заява. Кілька узгоджених — підтверджена сутність.</p>

<h2>Як читати результати</h2>

<p>Якщо провалилися пункти 1–4 — у вас проблема доступу. Найдешевша у виправленні й найшкідливіша, якщо її залишити.</p>

<p>Якщо 1–4 пройдені, а 5–8 ні — у вас проблема читабельності. Машини до вас дістаються, але не розуміють, що ви таке.</p>

<p>Якщо і це пройдено, а 11–12 слабкі — у вас проблема авторитетності, повільна. Технічною роботою її не скоротити.</p>

<h2>Три питання будь-якому підряднику</h2>

<p>Коли ви знаєте власні цифри, ці питання відділяють метод від театру:</p>

<p><strong>«Які з цих дванадцяти ви перевірили і що знайшли?»</strong> Справжній аудит покриває всі й показує докази.</p>

<p><strong>«Що входить у ціну, крім переліку проблем?»</strong> Діагноз без списку рішень — це половина продукту.</p>

<p><strong>«Що буде, якщо не спрацює?»</strong> <a href="/ua/blog/no-guaranteed-citations/">Той, хто гарантує цитування, обіцяє те, чого не контролює.</a></p>

<p>Якщо висновки підрядника збігаються з вашими власними, а він пояснює те, що ви перевірити не могли, — йому варто платити. Якщо його звіт розмитіший за вашу власну годину роботи, ви вже знаєте більше за нього.</p>"""
)}

# ------------------------------------------------------- связанные статьи
RELATED = {
    "geo-score-53-to-71":          ["we-audited-our-own-site", "security-headers-and-ai"],
    "no-guaranteed-citations":     ["geo-score-53-to-71", "geo-checklist-before-paying"],
    "brand-entity-for-ai":         ["eeat-for-ai-search", "how-ai-picks-sources"],
    "eeat-for-ai-search":          ["brand-entity-for-ai", "write-content-ai-quotes"],
    "how-ai-picks-sources":        ["google-ai-overviews", "brand-entity-for-ai"],
    "security-headers-and-ai":     ["ai-crawlers-guide", "geo-score-53-to-71"],
    "geo-checklist-before-paying": ["check-ai-visibility", "no-guaranteed-citations"],
}


def existing_meta(slug, lang):
    """Заголовок и описание уже опубликованной статьи — читаем прямо из файла."""
    base = "blog" if lang == "en" else "ua/blog"
    f = SITE / base / slug / "index.html"
    s = f.read_text(encoding="utf-8")
    h1 = re.search(r'<meta property="og:title" content="([^"]*)"', s).group(1)
    desc = re.search(r'<meta name="description" content="([^"]*)"', s).group(1)
    return h1, desc


def meta(slug, lang):
    if slug in P:
        _, h1, desc, _ = P[slug][lang]
        return h1, desc
    return existing_meta(slug, lang)


def build(slug, lang):
    title, h1, desc, body = P[slug][lang]
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

    cta = ('''<div class="post-cta">
  <p><strong>Want to know how AI assistants see your website?</strong> Run the free check — we reply with a summary of what ChatGPT, Perplexity and Gemini currently say about your business.</p>
  <a class="btn btn-primary" href="/#check">Check my website for free</a>
</div>''' if lang == "en" else '''<div class="post-cta">
  <p><strong>Хочете знати, як AI-асистенти бачать ваш сайт?</strong> Пройдіть безкоштовну перевірку — у відповідь підсумок того, що ChatGPT, Perplexity і Gemini зараз кажуть про ваш бізнес.</p>
  <a class="btn btn-primary" href="/ua/#check">Перевірити мій сайт безкоштовно</a>
</div>''')

    rel_items = ""
    for s in RELATED[slug]:
        rh1, rdesc = meta(s, lang)
        rel_items += f'''      <a class="blog-item" href="{base}{s}/">
        <h3>{rh1}</h3>
        <p>{rdesc}</p>
      </a>\n'''

    ld = json.dumps({
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Article", "@id": canon + "#article", "headline": h1, "description": desc,
             "inLanguage": "uk" if lang == "uk" else "en",
             "datePublished": iso, "dateModified": iso,
             "image": "https://mentio.agency/assets/og.png", "mainEntityOfPage": canon,
             "author": {"@id": "https://mentio.agency/#founder"},
             "publisher": {"@id": "https://mentio.agency/#org"},
             "speakable": {"@type": "SpeakableSpecification",
                           "cssSelector": ["h1", ".post-body p:first-of-type"]}},
            {"@type": "Person", "@id": "https://mentio.agency/#founder", "name": FOUNDER,
             "jobTitle": "Founder & GEO Consultant", "url": "https://mentio.agency/#founder",
             "description": "Founder of Mentio and Senior QA Engineer with a background in fintech, crypto, payments and blockchain. Applies QA methodology — reproducible checks and documented evidence — to Generative Engine Optimization audits.",
             "alumniOf": {"@type": "CollegeOrUniversity", "name": "Alfred Nobel University"},
             "sameAs": [FOUNDER_LI], "worksFor": {"@id": "https://mentio.agency/#org"},
             "knowsAbout": ["Generative Engine Optimization", "AI search visibility",
                            "Schema.org structured data", "llms.txt", "Quality assurance",
                            "Software testing"]},
            {"@type": "Organization", "@id": "https://mentio.agency/#org", "name": "Mentio",
             "url": "https://mentio.agency/", "email": "team@mentio.agency",
             "founder": {"@id": "https://mentio.agency/#founder"},
             "sameAs": SAME_AS,
             "logo": {"@type": "ImageObject", "url": "https://mentio.agency/assets/logo.png",
                      "width": 512, "height": 512}},
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
  <p class="post-meta"><a href="{blog}" style="color:inherit;text-decoration:none">{back}</a> · <a class="byline" href="{FOUNDER_LI}" rel="author noopener" target="_blank">{FOUNDER}</a> · {human(iso, lang)} · {rt}</p>
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


def main():
    # 1. статьи
    for slug, _ in NEW:
        for lang in ("en", "uk"):
            base = "blog" if lang == "en" else "ua/blog"
            d = SITE / base / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(build(slug, lang), encoding="utf-8")
        print("статья:", slug, DATES[slug])

    # 2. индексы блога — вставляем новые карточки сверху
    for lang in ("en", "uk"):
        idx = SITE / ("blog/index.html" if lang == "en" else "ua/blog/index.html")
        s = idx.read_text(encoding="utf-8")
        base = "/blog/" if lang == "en" else "/ua/blog/"
        cards = ""
        for slug, _ in sorted(NEW, key=lambda x: x[1], reverse=True):
            _, h1, desc, body = P[slug][lang]
            rt = f"{read_minutes(body)} min read" if lang == "en" else f"{read_minutes(body)} хв читання"
            cards += f'''    <a class="blog-item" href="{base}{slug}/">
      <p class="post-meta">{human(DATES[slug], lang)} · {rt}</p>
      <h3>{h1}</h3>
      <p>{desc}</p>
    </a>\n'''
        anchor = '<div class="blog-list">\n'
        i = s.index(anchor) + len(anchor)
        idx.write_text(s[:i] + cards + s[i:], encoding="utf-8")
        print("индекс блога обновлён:", idx.relative_to(SITE))

    # 3. sitemap
    sm = SITE / "sitemap.xml"
    x = sm.read_text(encoding="utf-8")
    add = ""
    for slug, iso in NEW:
        for base in ("/blog/", "/ua/blog/"):
            url = f"https://mentio.agency{base}{slug}/"
            if url not in x:
                add += f"  <url><loc>{url}</loc><lastmod>{iso}</lastmod><changefreq>monthly</changefreq><priority>0.7</priority></url>\n"
    if add:
        x = x.replace("</urlset>", add + "</urlset>")
        sm.write_text(x, encoding="utf-8")
    print("sitemap: добавлено URL:", add.count("<url>"))

    # 4. llms.txt + llms-full.txt — дописываем в секцию Blog
    for fn in ("llms.txt", "llms-full.txt"):
        f = SITE / fn
        t = f.read_text(encoding="utf-8")
        lines = ""
        for slug, _ in NEW:
            if f"/blog/{slug}/" in t:
                continue
            _, h1, desc, _ = P[slug]["en"]
            lines += f"- [{h1}](https://mentio.agency/blog/{slug}/): {desc}\n"
        if lines:
            m = re.search(r"\n\n##", t[t.index("## Blog"):])
            cut = t.index("## Blog") + m.start()
            t = t[:cut] + "\n" + lines.rstrip("\n") + t[cut:]
            f.write_text(t, encoding="utf-8")
            print(fn, "— добавлено строк:", lines.count("\n"))


if __name__ == "__main__":
    main()
