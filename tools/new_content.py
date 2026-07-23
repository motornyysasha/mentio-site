# -*- coding: utf-8 -*-
"""Content for the three new blog posts (EN + UA)."""

POSTS = {}

POSTS["ai-crawlers-guide"] = {
"en": dict(
  title="AI crawlers: which bots read your site and how to check they can — Mentio Blog",
  h1="AI crawlers: which bots read your site, and how to check they can",
  desc="GPTBot, ClaudeBot, PerplexityBot, Google-Extended — what each AI crawler does, how to check whether you're blocking them by accident, and which ones to allow.",
  body='''<p><strong>An AI crawler is a bot that fetches your pages so an AI system can read them</strong> — either to answer a user's question right now, or to build the index it answers from later. If your site blocks these bots, no amount of content or structured data matters: the model simply never sees you. This is the single most common, and most fixable, cause of AI invisibility we find in audits.</p>
<h2>The crawlers that matter</h2>
<table>
<tr><th>User agent</th><th>Who runs it</th><th>What it does</th></tr>
<tr><td><code>GPTBot</code></td><td>OpenAI</td><td>Collects pages for model training</td></tr>
<tr><td><code>OAI-SearchBot</code></td><td>OpenAI</td><td>Builds the index behind ChatGPT search results</td></tr>
<tr><td><code>ChatGPT-User</code></td><td>OpenAI</td><td>Fetches a page live when a user's question needs it</td></tr>
<tr><td><code>ClaudeBot</code></td><td>Anthropic</td><td>Crawls for Claude</td></tr>
<tr><td><code>PerplexityBot</code></td><td>Perplexity</td><td>Indexes pages for Perplexity answers</td></tr>
<tr><td><code>Google-Extended</code></td><td>Google</td><td>Controls use of your content in Gemini and AI features</td></tr>
<tr><td><code>Bingbot</code></td><td>Microsoft</td><td>Powers Bing, Copilot — and parts of ChatGPT search</td></tr>
<tr><td><code>Amazonbot</code>, <code>meta-externalagent</code>, <code>cohere-ai</code></td><td>Amazon, Meta, Cohere</td><td>Assistant and model crawlers</td></tr>
</table>
<p>Two distinctions worth understanding. First, <strong>training crawlers vs answer crawlers</strong>: GPTBot collects data for future models, while <code>ChatGPT-User</code> and <code>OAI-SearchBot</code> affect whether you can be cited <em>today</em>. Blocking the first is a business decision about your content; blocking the second is simply opting out of AI search. Second, <code>Google-Extended</code> is not a crawler at all — it's a permission token. Google's normal Googlebot still crawls you; the token only says whether that content may feed Gemini and AI features. Details are in <a href="https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers" rel="noopener">Google's crawler documentation</a> and <a href="https://platform.openai.com/docs/bots" rel="noopener">OpenAI's bot documentation</a>.</p>
<h2>How to check in 60 seconds</h2>
<p>Open <code>yoursite.com/robots.txt</code> in a browser. You are looking for two things:</p>
<ol>
<li><strong>Explicit blocks.</strong> Any line pairing one of the agents above with <code>Disallow: /</code> means that system is locked out entirely.</li>
<li><strong>A blanket block.</strong> A <code>User-agent: *</code> group with <code>Disallow: /</code> blocks everything that isn't explicitly allowed elsewhere — including every AI crawler.</li>
</ol>
<p>Also check for a <code>noindex</code> meta tag on key pages (view source, search for "noindex") and, if you can, an <code>X-Robots-Tag</code> header. A page can be perfectly crawlable and still be excluded by either.</p>
<h2>The three ways sites block AI by accident</h2>
<p><strong>Security plugins.</strong> WordPress security and anti-scraping plugins often ship "block AI bots" as a default-on feature. It's presented as protection; in practice it's an opt-out of AI search.</p>
<p><strong>CDN bot protection.</strong> Cloudflare and similar services have one-click toggles for blocking AI crawlers. Someone enables it for good reasons — bandwidth, content scraping — and nobody connects it to the marketing goal of being recommended by ChatGPT.</p>
<p><strong>Copy-pasted robots.txt.</strong> Templates from a few years ago block whole ranges of user agents. They get inherited from site to site, long after anyone remembers why.</p>
<h2>What we recommend allowing</h2>
<p>For almost every business whose goal is customers, the answer is: allow the answer-layer crawlers without hesitation (<code>OAI-SearchBot</code>, <code>ChatGPT-User</code>, <code>PerplexityBot</code>, <code>ClaudeBot</code>, <code>Bingbot</code>, <code>Google-Extended</code>). Being present in answers is exactly what you're trying to buy with all your other marketing.</p>
<p>Training crawlers (<code>GPTBot</code> and friends) are a genuine judgement call for publishers whose content <em>is</em> the product. For a service business, blocking them buys nothing and costs future recognition — models that learned your name during training can mention you even when browsing is off.</p>
<p>A minimal, permissive robots.txt looks like this:</p>
<pre><code>User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://yoursite.com/sitemap.xml</code></pre>
<h2>After you change it</h2>
<p>Crawlers re-read robots.txt on their own schedule — typically within days. To speed things up on the Bing side (which also feeds ChatGPT search), submit your URLs via <a href="https://www.indexnow.org" rel="noopener">IndexNow</a>. Then verify in your server or CDN logs that the bots actually return: if <code>GPTBot</code> and <code>PerplexityBot</code> start appearing in your access logs, the door is genuinely open.</p>
<h2>FAQ</h2>
<h3>Does allowing AI crawlers hurt my SEO?</h3>
<p>No. They are separate systems from Googlebot's ranking crawl. Allowing them adds AI visibility without touching your search rankings.</p>
<h3>Will AI bots overload my server?</h3>
<p>For a normal business site, their traffic is negligible — a few requests per day. High-volume publishers may want a crawl-delay; a ten-page service site will never notice.</p>
<h3>How do I know it worked?</h3>
<p>Run the <a href="/blog/check-ai-visibility/">5-minute visibility test</a> a couple of weeks later and compare. Crawler access is step 2 of that test for a reason: nothing downstream works without it.</p>''',
),
"uk": dict(
  title="AI-краулери: які боти читають ваш сайт і як перевірити доступ — Блог Mentio",
  h1="AI-краулери: які боти читають ваш сайт і як перевірити, що вони можуть",
  desc="GPTBot, ClaudeBot, PerplexityBot, Google-Extended — що робить кожен AI-краулер, як перевірити, чи не блокуєте ви їх випадково, і кого варто пускати.",
  body='''<p><strong>AI-краулер — це бот, який завантажує ваші сторінки, щоб AI-система могла їх прочитати</strong>: або щоб відповісти на питання користувача просто зараз, або щоб побудувати індекс, з якого відповідатиме пізніше. Якщо сайт блокує цих ботів, ніякий контент і жодна розмітка не мають значення: модель вас просто не бачить. Це найпоширеніша — і найлегше виправна — причина AI-невидимості, яку ми знаходимо в аудитах.</p>
<h2>Краулери, які мають значення</h2>
<table>
<tr><th>User agent</th><th>Хто запускає</th><th>Що робить</th></tr>
<tr><td><code>GPTBot</code></td><td>OpenAI</td><td>Збирає сторінки для навчання моделей</td></tr>
<tr><td><code>OAI-SearchBot</code></td><td>OpenAI</td><td>Будує індекс для пошуку в ChatGPT</td></tr>
<tr><td><code>ChatGPT-User</code></td><td>OpenAI</td><td>Завантажує сторінку наживо, коли цього потребує питання користувача</td></tr>
<tr><td><code>ClaudeBot</code></td><td>Anthropic</td><td>Сканує для Claude</td></tr>
<tr><td><code>PerplexityBot</code></td><td>Perplexity</td><td>Індексує сторінки для відповідей Perplexity</td></tr>
<tr><td><code>Google-Extended</code></td><td>Google</td><td>Керує використанням вашого контенту в Gemini та AI-функціях</td></tr>
<tr><td><code>Bingbot</code></td><td>Microsoft</td><td>Живить Bing, Copilot — і частину пошуку ChatGPT</td></tr>
<tr><td><code>Amazonbot</code>, <code>meta-externalagent</code>, <code>cohere-ai</code></td><td>Amazon, Meta, Cohere</td><td>Краулери асистентів і моделей</td></tr>
</table>
<p>Дві важливі відмінності. Перша: <strong>краулери навчання vs краулери відповідей</strong>. GPTBot збирає дані для майбутніх моделей, а <code>ChatGPT-User</code> і <code>OAI-SearchBot</code> впливають на те, чи можуть вас процитувати <em>сьогодні</em>. Блокувати перший — рішення про ваш контент; блокувати другий — це просто відмовитись від AI-пошуку. Друга: <code>Google-Extended</code> взагалі не краулер, а токен дозволу. Звичайний Googlebot сканує вас, як і раніше; токен лише каже, чи можна цей контент використовувати в Gemini та AI-функціях. Деталі — в <a href="https://developers.google.com/search/docs/crawling-indexing/overview-google-crawlers" rel="noopener">документації краулерів Google</a> і <a href="https://platform.openai.com/docs/bots" rel="noopener">документації ботів OpenAI</a>.</p>
<h2>Як перевірити за 60 секунд</h2>
<p>Відкрийте <code>vashsait.com/robots.txt</code> у браузері. Шукаєте дві речі:</p>
<ol>
<li><strong>Явні блокування.</strong> Будь-який рядок, що поєднує агента з таблиці вище і <code>Disallow: /</code>, означає: ця система закрита повністю.</li>
<li><strong>Суцільне блокування.</strong> Група <code>User-agent: *</code> з <code>Disallow: /</code> блокує все, що не дозволено явно деінде — включно з кожним AI-краулером.</li>
</ol>
<p>Ще перевірте мета-тег <code>noindex</code> на ключових сторінках (у коді сторінки знайдіть «noindex») і, якщо є доступ, заголовок <code>X-Robots-Tag</code>. Сторінка може ідеально скануватись і все одно бути виключеною будь-яким із них.</p>
<h2>Три способи випадково заблокувати AI</h2>
<p><strong>Плагіни безпеки.</strong> Плагіни захисту й анти-скрапінгу для WordPress часто мають «блокувати AI-ботів» увімкненим за замовчуванням. Подається як захист, а на практиці — відмова від AI-пошуку.</p>
<p><strong>Захист від ботів у CDN.</strong> У Cloudflare та подібних сервісів є перемикачі блокування AI-краулерів в один клік. Хтось вмикає їх із добрих міркувань — трафік, захист контенту — і ніхто не пов'язує це з маркетинговою метою бути в рекомендаціях ChatGPT.</p>
<p><strong>Скопійований robots.txt.</strong> Шаблони кількарічної давнини блокують цілі списки агентів. Вони переходять із сайту на сайт довго після того, як усі забули навіщо.</p>
<h2>Що ми радимо дозволяти</h2>
<p>Майже для кожного бізнесу, чия мета — клієнти, відповідь така: без вагань дозволяйте краулери шару відповідей (<code>OAI-SearchBot</code>, <code>ChatGPT-User</code>, <code>PerplexityBot</code>, <code>ClaudeBot</code>, <code>Bingbot</code>, <code>Google-Extended</code>). Присутність у відповідях — саме те, що ви намагаєтесь купити всім іншим маркетингом.</p>
<p>Краулери навчання (<code>GPTBot</code> і компанія) — справді предмет вибору для видавців, чий контент <em>і є</em> продуктом. Для сервісного бізнесу їх блокування не дає нічого, але коштує майбутньої впізнаваності: моделі, які вивчили вашу назву під час навчання, можуть згадати вас навіть із вимкненим браузингом.</p>
<p>Мінімальний дозвільний robots.txt виглядає так:</p>
<pre><code>User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: https://vashsait.com/sitemap.xml</code></pre>
<h2>Після зміни</h2>
<p>Краулери перечитують robots.txt за власним графіком — зазвичай упродовж кількох днів. Щоб прискорити на боці Bing (який живить і пошук ChatGPT), надішліть свої URL через <a href="https://www.indexnow.org" rel="noopener">IndexNow</a>. Далі перевірте в логах сервера чи CDN, що боти справді повертаються: якщо <code>GPTBot</code> і <code>PerplexityBot</code> почали з'являтись у логах доступу — двері справді відчинені.</p>
<h2>FAQ</h2>
<h3>Чи зашкодить дозвіл AI-краулерів моєму SEO?</h3>
<p>Ні. Це окремі системи від ранжувального сканування Googlebot. Дозвіл додає AI-видимість, не торкаючись ваших позицій.</p>
<h3>Чи не перевантажать AI-боти сервер?</h3>
<p>Для звичайного бізнес-сайту їхній трафік мізерний — кілька запитів на день. Великим видавцям може знадобитись crawl-delay; сайт із десяти сторінок цього навіть не помітить.</p>
<h3>Як зрозуміти, що спрацювало?</h3>
<p>Через пару тижнів пройдіть <a href="/ua/blog/check-ai-visibility/">тест видимості на 5 хвилин</a> і порівняйте. Доступ краулерів — крок 2 того тесту невипадково: без нього не працює нічого далі.</p>''',
),
}

POSTS["schema-for-ai"] = {
"en": dict(
  title="Schema.org for AI search: the 5 types that actually matter — Mentio Blog",
  h1="Schema.org for AI search: the 5 types that actually matter",
  desc="Structured data is how you state facts machines can trust. Which schema types move the needle for AI visibility, what to put in them, and the mistake that quietly cancels them out.",
  body='''<p><strong>Structured data is a machine-readable statement of facts about your page, written in JSON-LD and embedded in the HTML.</strong> For classic SEO it earned rich snippets. For AI search it does something more fundamental: it lets a model confirm who you are, what you sell and what it costs — before deciding whether it's safe to say that in an answer. Models are conservative. Unconfirmed facts get left out.</p>
<p>Schema.org has hundreds of types. Five of them do almost all the work.</p>
<h2>1. Organization — the one nobody should skip</h2>
<p>This is your identity record: name, URL, logo, contact, and — critically — <code>sameAs</code>, the list of your profiles elsewhere. <code>sameAs</code> is what turns a name on a page into a recognized entity: it lets a model connect your site to your LinkedIn, your GitHub, your directory listings, and confirm they are the same business. If your brand name is shared with other companies (ours is), this is the difference between being described accurately and being confused with someone else.</p>
<pre><code>{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://yoursite.com/#org",
  "name": "Your Business",
  "url": "https://yoursite.com/",
  "logo": "https://yoursite.com/logo.png",
  "email": "hello@yoursite.com",
  "sameAs": [
    "https://www.linkedin.com/company/your-business/",
    "https://www.google.com/maps/place/..."
  ]
}</code></pre>
<h2>2. LocalBusiness — if customers come to you</h2>
<p>A subtype of Organization with the facts local queries turn on: <code>address</code>, <code>telephone</code>, <code>geo</code>, <code>openingHoursSpecification</code>, <code>priceRange</code>. When someone asks an assistant for "the best X near me", these are the fields the answer is assembled from. Make sure every one of them matches your Google Business Profile exactly — contradictions between sources are read as low trust.</p>
<h2>3. Service and Offer — what you sell, at what price</h2>
<p>Prices are the single most quotable fact a business has, and most sites hide them from machines by putting them only in an image or a PDF. A <code>Service</code> with an <code>Offer</code> that carries <code>price</code> and <code>priceCurrency</code> states it plainly. Our own site does exactly this for its $99 audit, which is why an assistant can answer "how much does a Mentio audit cost" without guessing.</p>
<h2>4. FAQPage — clean question-answer pairs</h2>
<p>Google restricted FAQ rich results to a narrow set of sites in 2023, so the SEO payoff is mostly gone. Keep the markup anyway: it hands language models perfectly delimited Q&amp;A pairs, in your words, on the questions you chose. It costs nothing and it's some of the most liftable content on your page.</p>
<h2>5. Article — for anything you publish</h2>
<p><code>headline</code>, <code>datePublished</code>, <code>dateModified</code>, <code>author</code>, <code>publisher</code>. Two details matter more than people expect. First, the dates: freshness is a real citation signal, and an article with no date is harder to trust. Second, the author — an <code>@type: Person</code> with a real name and a <code>sameAs</code> link is a stronger E-E-A-T signal than an anonymous organization byline.</p>
<h2>The mistake that cancels it all out</h2>
<p><strong>Markup that doesn't match the visible page.</strong> If your JSON-LD says the price is $99 and the page says "contact us for pricing", you haven't confirmed a fact — you've created a contradiction, and a conservative model resolves contradictions by staying silent about you. Structured data is a mirror of the page, not a place to put claims the page doesn't make. Google says the same thing in its <a href="https://developers.google.com/search/docs/appearance/structured-data/sd-policies" rel="noopener">structured data guidelines</a>.</p>
<p>Two smaller but common issues: multiple Organization definitions across pages that aren't linked by a shared <code>@id</code> (fragmenting your entity into several half-entities), and markup that validates but sits inside a page the crawler can't reach.</p>
<h2>How to check yours</h2>
<p>Paste your URL into <a href="https://validator.schema.org" rel="noopener">validator.schema.org</a> for correctness, and Google's Rich Results Test for eligibility. Read the output as three questions: is there any structured data at all; does it identify the business with contacts and <code>sameAs</code>; does everything in it also appear on the visible page?</p>
<h2>FAQ</h2>
<h3>JSON-LD, Microdata or RDFa?</h3>
<p>JSON-LD. It's Google's recommended format, it sits in one block in the head, and it doesn't entangle your markup with your layout.</p>
<h3>Do I need every type?</h3>
<p>No. Organization is mandatory in practice; add LocalBusiness if you have a location, Service/Offer if you have priced services, FAQPage and Article if you have that content. Types you don't genuinely have are noise.</p>
<h3>Will structured data alone get me cited?</h3>
<p>No — it removes a reason not to cite you. Access, citable content and off-site mentions still do the rest, which is why our <a href="/#services">$99 audit</a> checks all four layers rather than just the markup.</p>''',
),
"uk": dict(
  title="Schema.org для AI-пошуку: 5 типів, які справді важать — Блог Mentio",
  h1="Schema.org для AI-пошуку: 5 типів, які справді важать",
  desc="Структуровані дані — це спосіб заявити факти, яким машина може довіряти. Які типи розмітки реально впливають на AI-видимість, що в них писати і яка помилка тихо все знецінює.",
  body='''<p><strong>Структуровані дані — це машиночитаний виклад фактів про вашу сторінку у форматі JSON-LD, вбудований у HTML.</strong> Для класичного SEO вони давали розширені сніпети. Для AI-пошуку вони роблять щось фундаментальніше: дозволяють моделі підтвердити, хто ви, що продаєте і скільки це коштує — перш ніж вирішити, чи безпечно сказати це у відповіді. Моделі обережні. Непідтверджені факти вони пропускають.</p>
<p>У Schema.org сотні типів. П'ять із них роблять майже всю роботу.</p>
<h2>1. Organization — той, який не можна пропускати</h2>
<p>Це ваш запис ідентичності: назва, URL, логотип, контакти і — критично — <code>sameAs</code>, список ваших профілів деінде. Саме <code>sameAs</code> перетворює назву на сторінці на впізнану сутність: він дозволяє моделі пов'язати ваш сайт з вашим LinkedIn, GitHub, профілями в каталогах і підтвердити, що це один і той самий бізнес. Якщо назву вашого бренду поділяють інші компанії (як у нас), це різниця між точним описом і плутаниною з кимось іншим.</p>
<pre><code>{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://vashsait.com/#org",
  "name": "Ваш бізнес",
  "url": "https://vashsait.com/",
  "logo": "https://vashsait.com/logo.png",
  "email": "hello@vashsait.com",
  "sameAs": [
    "https://www.linkedin.com/company/vash-biznes/",
    "https://www.google.com/maps/place/..."
  ]
}</code></pre>
<h2>2. LocalBusiness — якщо клієнти приходять до вас</h2>
<p>Підтип Organization із фактами, на яких тримаються локальні запити: <code>address</code>, <code>telephone</code>, <code>geo</code>, <code>openingHoursSpecification</code>, <code>priceRange</code>. Коли хтось питає асистента про «найкращий X поруч зі мною», відповідь збирається саме з цих полів. Переконайтесь, що кожне з них точно збігається з вашим Google Business Profile — суперечності між джерелами читаються як низька довіра.</p>
<h2>3. Service і Offer — що продаєте і за скільки</h2>
<p>Ціна — найцитованіший факт, який має бізнес, і більшість сайтів ховає її від машин, розміщуючи лише на картинці чи в PDF. <code>Service</code> з <code>Offer</code>, що містить <code>price</code> і <code>priceCurrency</code>, викладає її прямо. Наш власний сайт робить саме це для аудиту за $99 — тому асистент може відповісти «скільки коштує аудит Mentio», не вгадуючи.</p>
<h2>4. FAQPage — чисті пари «питання-відповідь»</h2>
<p>Google обмежив розширені FAQ-результати вузьким колом сайтів у 2023 році, тож SEO-вигода майже зникла. Розмітку все одно лишайте: вона дає мовним моделям ідеально розділені пари Q&amp;A — вашими словами, на питаннях, які обрали ви. Це нічого не коштує і є одним із найзручніших для цитування блоків сторінки.</p>
<h2>5. Article — для всього, що публікуєте</h2>
<p><code>headline</code>, <code>datePublished</code>, <code>dateModified</code>, <code>author</code>, <code>publisher</code>. Дві деталі важать більше, ніж здається. Перша — дати: свіжість є реальним сигналом для цитування, а статті без дати важче довіряти. Друга — автор: <code>@type: Person</code> зі справжнім іменем і посиланням <code>sameAs</code> — значно сильніший E-E-A-T сигнал, ніж анонімний підпис організації.</p>
<h2>Помилка, яка знецінює все</h2>
<p><strong>Розмітка, що не збігається з видимою сторінкою.</strong> Якщо ваш JSON-LD каже, що ціна $99, а сторінка каже «ціна за запитом» — ви не підтвердили факт, ви створили суперечність. А обережна модель вирішує суперечності мовчанням про вас. Структуровані дані — дзеркало сторінки, а не місце для тверджень, яких на сторінці немає. Те саме пише Google у своїх <a href="https://developers.google.com/search/docs/appearance/structured-data/sd-policies" rel="noopener">рекомендаціях щодо структурованих даних</a>.</p>
<p>Дві менші, але часті проблеми: кілька визначень Organization на різних сторінках, не пов'язаних спільним <code>@id</code> (це дробить вашу сутність на кілька напів-сутностей), і валідна розмітка на сторінці, до якої краулер не може дістатись.</p>
<h2>Як перевірити свою</h2>
<p>Вставте URL у <a href="https://validator.schema.org" rel="noopener">validator.schema.org</a> для перевірки коректності і в Rich Results Test від Google — для придатності. Читайте результат як три питання: чи є розмітка взагалі; чи ідентифікує вона бізнес із контактами і <code>sameAs</code>; чи все в ній є також на видимій сторінці?</p>
<h2>FAQ</h2>
<h3>JSON-LD, Microdata чи RDFa?</h3>
<p>JSON-LD. Це рекомендований Google формат, він живе одним блоком у head і не переплітає розмітку з версткою.</p>
<h3>Чи потрібні всі типи?</h3>
<p>Ні. Organization обов'язковий на практиці; додайте LocalBusiness, якщо є локація, Service/Offer — якщо є послуги з цінами, FAQPage і Article — якщо є такий контент. Типи, яких у вас насправді немає, — це шум.</p>
<h3>Чи достатньо самої розмітки, щоб вас цитували?</h3>
<p>Ні — вона прибирає причину вас не цитувати. Доступ, цитований контент і зовнішні згадки роблять решту. Саме тому наш <a href="/ua/#services">аудит за $99</a> перевіряє всі чотири шари, а не лише розмітку.</p>''',
),
}

POSTS["write-content-ai-quotes"] = {
"en": dict(
  title="How to write content AI actually quotes — Mentio Blog",
  h1="How to write content AI actually quotes",
  desc="Assistants lift specific, self-contained passages — not paragraphs of positioning. Six concrete rules, with before-and-after examples, for making your pages quotable.",
  body='''<p><strong>An AI answer is assembled from passages, not pages.</strong> The model scans what it retrieved, picks two to five fragments that directly answer the question, and rewrites them into a paragraph with citations. So the practical question isn't "is my page good" — it's "does my page contain sentences worth lifting?" Most marketing copy, honestly, does not.</p>
<p>Six rules turn ordinary pages into quotable ones. None of them require rewriting your site.</p>
<h2>1. Answer in the first sentence</h2>
<p>Put the direct answer immediately after the heading, before any context or story. A model reading for an answer keeps the first self-contained statement it finds; a human skimming appreciates the same thing.</p>
<p><strong>Before:</strong> "In today's competitive market, choosing the right dental implant provider can feel overwhelming. There are many factors to consider…"<br>
<strong>After:</strong> "A single dental implant in Austin costs $1,900–$2,400 and takes two visits over three months."</p>
<h2>2. Numbers instead of adjectives</h2>
<p>"Affordable", "fast", "leading" carry no information a model can quote. Prices, ranges, durations, quantities, percentages do. Every adjective in your copy is a place where a number could go — and every number you publish is a sentence an assistant can safely repeat.</p>
<h2>3. Write headings as the questions people ask</h2>
<p>"Pricing" is a label. "How much does an implant cost?" is a retrieval target. The closer your headings sit to actual phrasing, the more likely the passage beneath them gets matched to a real query. Read your headings aloud: if nobody would ever say them out loud, rewrite them.</p>
<h2>4. Keep passages self-contained</h2>
<p>A quotable passage stands alone without the sentence before it. Avoid opening with "This means that…", "As mentioned above…", or a pronoun whose subject is two paragraphs up. Repeat the subject instead — "GEO audits", not "it". Slightly more repetitive for a human reader; dramatically more liftable for a machine.</p>
<h2>5. Use structure the parser can see</h2>
<p>Tables for comparisons, ordered lists for processes, one idea per paragraph of two to four sentences. Structure isn't decoration: it tells a model where a fragment begins and ends. A wall of text has no seams, so it gets skipped in favor of a competitor's neat table.</p>
<h2>6. Show your work, and date it</h2>
<p>Original numbers, dated observations and named sources are what distinguish a citable page from a rewritten one. "We audited 40 clinic websites in March; 27 blocked at least one AI crawler" is a sentence only you can publish — which makes it exactly the kind of sentence that earns citations. Add <code>datePublished</code> in your <a href="/blog/schema-for-ai/">structured data</a> so the freshness is machine-visible too.</p>
<h2>A quick self-test</h2>
<p>Open your most important page and try to find three sentences that would survive being pasted into someone else's answer, verbatim, with a link back to you. If you can't find three, the page isn't citable yet — regardless of how well it reads.</p>
<h2>What not to do</h2>
<p><strong>Don't stuff.</strong> Repeating "best GEO agency in Kyiv" fifteen times worked on 2012 search engines and works on nothing today; models weight clarity, not density.</p>
<p><strong>Don't hide facts in images.</strong> Price lists as JPEGs, specs inside PDFs, key terms baked into graphics — all invisible to the layer you're trying to reach.</p>
<p><strong>Don't publish claims you can't source.</strong> An unsourced statistic is a liability twice over: it weakens trust with human readers, and it's the kind of statement a careful model declines to repeat.</p>
<h2>FAQ</h2>
<h3>Does length matter?</h3>
<p>Only through clarity. A 600-word page with four concrete, self-contained answers outperforms 3,000 words of positioning. Depth helps when it adds facts, not when it adds words.</p>
<h3>Should I write for AI or for people?</h3>
<p>The same text, if you do it right. Every rule above — answer first, real numbers, plain headings, short paragraphs — is what makes copy better for humans too. GEO isn't a separate writing style; it's disciplined writing.</p>
<h3>How do I know if it's working?</h3>
<p>Ask the assistants the questions your pages answer, and see whether your phrasing comes back. That's the loop the <a href="/blog/check-ai-visibility/">5-minute test</a> formalizes.</p>''',
),
"uk": dict(
  title="Як писати контент, який AI справді цитує — Блог Mentio",
  h1="Як писати контент, який AI справді цитує",
  desc="Асистенти беруть конкретні самодостатні фрагменти, а не абзаци позиціонування. Шість правил із прикладами «до і після», щоб ваші сторінки стали цитованими.",
  body='''<p><strong>AI-відповідь збирається з фрагментів, а не зі сторінок.</strong> Модель переглядає знайдене, обирає два-п'ять уривків, які прямо відповідають на питання, і переписує їх в абзац із цитуванням. Тому практичне питання не «чи хороша моя сторінка», а «чи є на ній речення, варті цитування?». Чесно кажучи, більшість маркетингових текстів таких речень не має.</p>
<p>Шість правил перетворюють звичайні сторінки на цитовані. Жодне з них не вимагає переписувати сайт.</p>
<h2>1. Відповідайте в першому реченні</h2>
<p>Ставте пряму відповідь одразу після заголовка, до будь-якого контексту й історії. Модель, що читає заради відповіді, бере перше самодостатнє твердження, яке знаходить; людина, що гортає, цінує те саме.</p>
<p><strong>Було:</strong> «У сучасному конкурентному ринку вибір правильної клініки імплантації може здаватись складним. Є багато факторів…»<br>
<strong>Стало:</strong> «Один зубний імплант у Львові коштує 45–60 тис. грн і потребує двох візитів упродовж трьох місяців.»</p>
<h2>2. Цифри замість прикметників</h2>
<p>«Доступно», «швидко», «провідний» не несуть інформації, яку модель може процитувати. Ціни, діапазони, терміни, кількості, відсотки — несуть. Кожен прикметник у вашому тексті — це місце, де могла б стояти цифра. А кожна опублікована цифра — це речення, яке асистент може безпечно повторити.</p>
<h2>3. Пишіть заголовки як питання, які ставлять люди</h2>
<p>«Ціни» — це ярлик. «Скільки коштує імплант?» — це ціль для пошуку. Чим ближче ваші заголовки до реальних формулювань, тим імовірніше фрагмент під ними зіставиться зі справжнім запитом. Прочитайте свої заголовки вголос: якщо ніхто ніколи так не скаже — перепишіть.</p>
<h2>4. Робіть фрагменти самодостатніми</h2>
<p>Цитований фрагмент стоїть окремо, без попереднього речення. Уникайте початків «Це означає, що…», «Як згадано вище…» чи займенника, чий суб'єкт двома абзацами вище. Краще повторіть суб'єкт — «GEO-аудит», а не «він». Трохи більше повторів для людини; значно краща цитованість для машини.</p>
<h2>5. Використовуйте структуру, яку бачить парсер</h2>
<p>Таблиці для порівнянь, нумеровані списки для процесів, одна думка на абзац із двох-чотирьох речень. Структура — не прикраса: вона каже моделі, де фрагмент починається і де закінчується. Суцільна стіна тексту не має швів, тож її пропускають на користь охайної таблиці конкурента.</p>
<h2>6. Показуйте свою роботу і ставте дати</h2>
<p>Власні цифри, датовані спостереження і названі джерела — те, що відрізняє цитовану сторінку від переписаної. «Ми перевірили 40 сайтів клінік у березні; 27 блокували щонайменше одного AI-краулера» — речення, яке можете опублікувати лише ви. Саме такі речення й заробляють цитати. Додайте <code>datePublished</code> у <a href="/ua/blog/schema-for-ai/">структуровані дані</a>, щоб свіжість була видима і машині.</p>
<h2>Швидкий самотест</h2>
<p>Відкрийте найважливішу сторінку і спробуйте знайти три речення, які пережили б вставку в чужу відповідь дослівно, з посиланням на вас. Якщо трьох не знаходиться — сторінка ще не цитована, хай як добре вона читається.</p>
<h2>Чого не робити</h2>
<p><strong>Не набивайте ключі.</strong> Повторити «найкраща GEO-агенція у Києві» п'ятнадцять разів працювало на пошуковиках 2012 року і не працює сьогодні ніде: моделі зважують ясність, а не щільність.</p>
<p><strong>Не ховайте факти в картинках.</strong> Прайси в JPEG, характеристики в PDF, ключові терміни, вбудовані у графіку — усе це невидиме для шару, до якого ви прагнете.</p>
<p><strong>Не публікуйте тверджень без джерел.</strong> Статистика без посилання шкодить двічі: підриває довіру людей і стає саме тим твердженням, яке обережна модель відмовляється повторювати.</p>
<h2>FAQ</h2>
<h3>Чи важлива довжина?</h3>
<p>Лише через ясність. Сторінка на 600 слів із чотирма конкретними самодостатніми відповідями обійде 3000 слів позиціонування. Глибина допомагає, коли додає факти, а не слова.</p>
<h3>Писати для AI чи для людей?</h3>
<p>Один і той самий текст, якщо робити правильно. Кожне правило вище — відповідь спершу, реальні цифри, прості заголовки, короткі абзаци — робить текст кращим і для людей. GEO — не окремий стиль письма, це дисциплінований текст.</p>
<h3>Як зрозуміти, що працює?</h3>
<p>Спитайте асистентів те, на що відповідають ваші сторінки, і подивіться, чи повертаються ваші формулювання. Саме цей цикл формалізує <a href="/ua/blog/check-ai-visibility/">тест на 5 хвилин</a>.</p>''',
),
}
