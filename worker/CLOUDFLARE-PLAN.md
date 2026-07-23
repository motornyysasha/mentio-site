# Шаг 5 аудита: security-заголовки через Cloudflare

Цель: закрыть проблему №4 («Немає security-заголовків», технический компонент 60/100).
GitHub Pages свои заголовки отдавать не умеет — нужен прокси перед ним.

Бэкап DNS до переноса: [DNS-BACKUP-godaddy-2026-07-23.md](DNS-BACKUP-godaddy-2026-07-23.md)

---

## ВЫПОЛНЕНО 23 июля 2026

Аккаунт Cloudflare `023fe014d538d79ce21a4719bf9c7b1c`, зона `4aed79d5f6bb3de7c03e197967a2b5d1`, план Free.
NS в GoDaddy заменены на `martin.ns.cloudflare.com` / `susan.ns.cloudflare.com`.

Что вскрылось по ходу и чем отличается от плана:

1. **Автоимпорт перенёс 12 записей из 14** — молча пропустил оба DKIM
   (`secureserver1._domainkey`, `secureserver2._domainkey`). Добавлены руками.
   Именно ради этого и снимался бэкап: через `dig` эти селекторы не угадываются.
2. **Две записи импортировались проксированными, хотя не должны**: `email` (вебмейл GoDaddy)
   и `_domainconnect`. Переведены в DNS only.
3. **Onboarding Cloudflare по умолчанию блокирует AI-краулеров обучения и дописывает запрет
   в robots.txt.** Для GEO-агентства это противоречит и собственному robots.txt, и статьям
   в блоге. Search / Agent / Training выставлены в **Allow**, тумблер robots.txt — **выключен**.
4. **SSL оставлен Full, а не Full (strict).** У связки GitHub Pages + Cloudflare известны срывы
   автопродления сертификата; strict в такой момент положил бы сайт, а выигрыш в безопасности
   здесь околонулевой — origin это IP самого GitHub.
5. **CSP из плана аудита не подошёл**: `default-src 'self'` без исключений заблокировал бы
   GoatCounter и отправку лидов в Telegram. Итоговый вариант ниже — три внешних origin, не больше.
6. **Добавлен `Permissions-Policy`**, которого в плане аудита не было.
7. DNSSEC проверен — не активен, переключение безопасно.

HSTS включается отдельно, последним, после проверки живого сайта.

---

## Порядок действий

### 1. Добавить домен в Cloudflare
dash.cloudflare.com → Add a domain → `mentio.agency` → план **Free**.
Cloudflare сканирует зону и импортирует записи.

### 2. СВЕРИТЬ записи — до смены NS
Самый важный шаг. Сверить импортированное с бэкапом (17 записей).
Особый контроль за теми, что автоимпорт пропускает чаще всего:

| Тип | Имя | Значение |
|---|---|---|
| CNAME | `secureserver1._domainkey` | `s1.dkim.mentio_agency.be6.onsecureserver.net.` |
| CNAME | `secureserver2._domainkey` | `s2.dkim.mentio_agency.be6.onsecureserver.net.` |
| SRV | `_autodiscover._tcp` | `0 0 443 autodiscover.secureserver.net.` |
| MX | `@` | `smtp.secureserver.net.` (0), `mailstore1.secureserver.net.` (10) |
| TXT | `@` | `v=spf1 include:secureserver.net -all` |
| TXT | `_dmarc` | `v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;` |
| CNAME | `email` | `email.secureserver.net.` |

Чего нет — добавить руками. **Пока не совпадёт всё — NS не менять.**

### 3. Облака
- Оранжевое (проксируется): 4× A `@` → 185.199.108–111.153, CNAME `www` → motornyysasha.github.io
- Серое (DNS only): **все почтовые** — MX, SPF, DKIM, DMARC, `email`, `_autodiscover`

Проксировать почтовую запись = сломать почту. Это единственная реальная опасность переноса.

### 4. Сменить NS в GoDaddy
GoDaddy → mentio.agency → DNS → Nameservers → Change → «I'll use my own nameservers»
→ вписать пару, которую выдал Cloudflare (вида `xxx.ns.cloudflare.com`).
Активация обычно 5–30 минут, иногда до нескольких часов.

### 5. SSL/TLS
- SSL/TLS → Overview → режим **Full (strict)** (у GitHub Pages валидный сертификат, strict работает)
- Edge Certificates → **Always Use HTTPS** = On
- Edge Certificates → **HSTS** = On, max-age 6 месяцев, Include subdomains: **off** на старте

> HSTS включать последним, после того как сайт проверен и работает по HTTPS.
> Откатить его нельзя мгновенно — браузеры кешируют политику на весь max-age.

### 6. Заголовки: Rules → Transform Rules → Modify Response Header
Одно правило, «All incoming requests», четыре Set:

| Заголовок | Значение |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), interest-cohort=()` |
| `Content-Security-Policy` | см. ниже |

### CSP под реальные ресурсы сайта

```
default-src 'self'; script-src 'self' https://gc.zgo.at; connect-src 'self' https://cool-waterfall-a3ce.motornyysasha.workers.dev https://mentio.goatcounter.com; img-src 'self' data: https://mentio.goatcounter.com; style-src 'self' 'unsafe-inline'; font-src 'self'; base-uri 'self'; form-action 'self'; frame-ancestors 'none'; object-src 'none'; upgrade-insecure-requests
```

Откуда что:
- `gc.zgo.at` — скрипт GoatCounter (`<script src="https://gc.zgo.at/count.js">`)
- `mentio.goatcounter.com` — туда уходит пиксель с хитом (нужен и в `img-src`, и в `connect-src`)
- `cool-waterfall-a3ce.motornyysasha.workers.dev` — Worker, принимающий лиды из форм
- `'unsafe-inline'` **только для style** — на сайте есть inline `style="..."`, а site.js правит `element.style`
- для `script-src` `'unsafe-inline'` **не нужен**: inline-JS на сайте нет вообще, JSON-LD не исполняется
- `frame-ancestors 'none'` заменяет устаревший `X-Frame-Options`

Из плана аудита CSP взят не дословно: предложенный там `default-src 'self'` без
исключений заблокировал бы аналитику и отправку лидов.

### 7. Проверка

```bash
curl -sI https://mentio.agency | grep -iE 'strict-transport|content-type-options|content-security|referrer|permissions'
```

Затем обязательно проклик живого сайта с открытой консолью:
- главная (демо-чат в hero, marquee)
- квиз и калькулятор
- **отправка формы → лид дошёл в Telegram**
- блог, смена языка

Любая ошибка вида `Refused to … because it violates the following Content Security Policy directive`
= в CSP не хватает источника. Дополнить и передеплоить правило.

### 8. Проверка почты после переноса

```bash
dig +short mentio.agency MX
dig +short mentio.agency TXT
dig +short secureserver1._domainkey.mentio.agency CNAME
```

И живой тест: отправить письмо на team@mentio.agency с внешнего адреса и ответить с него же.

---

## Откат

GoDaddy → Nameservers → вернуть `ns27.domaincontrol.com` / `ns28.domaincontrol.com`.
Зона в GoDaddy при смене NS сохраняется, поэтому откат возвращает прежнее состояние.

## Альтернатива, если переносить NS не хочется

Перенести хостинг с GitHub Pages на Netlify или Cloudflare Pages — оба отдают
кастомные заголовки из файла `_headers` в репозитории, DNS остаётся у GoDaddy,
почта не затрагивается вообще. Меняются только A/CNAME записи сайта.
Дороже по трудозатратам, но радиус поражения при ошибке меньше.
