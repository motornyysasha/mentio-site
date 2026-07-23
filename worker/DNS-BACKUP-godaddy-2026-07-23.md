# DNS mentio.agency — снимок перед переносом на Cloudflare

Снято с GoDaddy 23 июля 2026, до смены NS. **17 записей.**
Если после переноса что-то потеряется — восстанавливать по этой таблице.

| # | Тип | Имя | Значение | TTL |
|---|---|---|---|---|
| 1 | A | @ | 185.199.108.153 | 600 |
| 2 | A | @ | 185.199.109.153 | 600 |
| 3 | A | @ | 185.199.110.153 | 600 |
| 4 | A | @ | 185.199.111.153 | 600 |
| 5 | NS | @ | ns27.domaincontrol.com. | 1h |
| 6 | NS | @ | ns28.domaincontrol.com. | 1h |
| 7 | CNAME | email | email.secureserver.net. | 1h |
| 8 | CNAME | secureserver1._domainkey | s1.dkim.mentio_agency.be6.onsecureserver.net. | 1h |
| 9 | CNAME | secureserver2._domainkey | s2.dkim.mentio_agency.be6.onsecureserver.net. | 1h |
| 10 | CNAME | www | motornyysasha.github.io. | 1h |
| 11 | CNAME | _domainconnect | _domainconnect.gd.domaincontrol.com. | 1h |
| 12 | SOA | @ | ns27.domaincontrol.com. (генерится автоматически) | 1h |
| 13 | MX | @ | smtp.secureserver.net. (приоритет 0) | 1h |
| 14 | MX | @ | mailstore1.secureserver.net. (приоритет 10) | 1h |
| 15 | TXT | @ | `v=spf1 include:secureserver.net -all` | 1h |
| 16 | TXT | _dmarc | `v=DMARC1; p=quarantine; adkim=r; aspf=r; rua=mailto:dmarc_rua@onsecureserver.net;` | 1h |
| 17 | SRV | _autodiscover._tcp.@ | 0 0 443 autodiscover.secureserver.net. | 1h |

## Что критично для почты (team@mentio.agency)

Записи 7, 8, 9, 13, 14, 15, 16, 17. Если пропадёт любая из них — почта либо перестанет
ходить, либо начнёт улетать в спам. Проверять их наличие в Cloudflare **до** смены NS.

Особое внимание: **8 и 9 (DKIM)** и **17 (SRV)** — их автоимпорт Cloudflare
пропускает чаще всего, потому что селекторы нестандартные, а SRV сканер часто не видит.

## Что относится к сайту

Записи 1–4 (A на GitHub Pages) и 10 (www → motornyysasha.github.io).
Только на них включается оранжевое облако (проксирование). На всех почтовых —
облако **серое**, иначе почта сломается.

Запись 11 (`_domainconnect`) — служебная для GoDaddy-автонастройки, после переноса
не нужна, но и не мешает.
Запись 12 (SOA) и 5–6 (NS) в Cloudflare не переносятся — он создаёт свои.

## Откат

GoDaddy → DNS → Nameservers → вернуть `ns27.domaincontrol.com` и `ns28.domaincontrol.com`.
Записи в зоне GoDaddy при смене NS не удаляются, поэтому откат возвращает всё как было
(с задержкой на распространение DNS).
