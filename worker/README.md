# Лиды с mentio.agency → Telegram

Формы сайта (сканер и тест AI Visibility) отправляют лиды POST-запросом на Cloudflare Worker,
а он пересылает их сообщением в Telegram. Токен бота хранится в секретах Worker — на сайте его нет.

Пока Worker не подключён, сайт автоматически работает в старом режиме (mailto).

## Настройка (~10 минут, всё бесплатно)

### 1. Создать Telegram-бота
1. Открой в Telegram **@BotFather** → команда `/newbot` → придумай имя (например, `Mentio Leads`) и username (например, `mentio_leads_bot`).
2. BotFather пришлёт **токен** вида `1234567890:AA...` — не отправляй его никому, он понадобится только в шаге 3.
3. Открой **@userinfobot** → он покажет твой **chat id** (число вида `123456789`).
4. Напиши своему новому боту любое сообщение (например, «привет») — без этого бот не сможет писать тебе первым.

### 2. Создать Cloudflare Worker
1. Зарегистрируйся на https://dash.cloudflare.com (бесплатный план).
2. Workers & Pages → **Create** → **Create Worker** → имя, например `mentio-leads` → **Deploy**.
3. Нажми **Edit code**, удали всё и вставь содержимое файла `telegram-worker.js` из этой папки → **Deploy**.

### 3. Добавить секреты
Worker → **Settings** → **Variables and Secrets** → добавь два секрета (тип **Secret**):
- `TG_TOKEN` — токен бота из шага 1
- `TG_CHAT` — твой chat id из шага 1

### 4. Подключить к сайту
Скопируй URL воркера (вида `https://mentio-leads.<аккаунт>.workers.dev`) и передай его Claude —
он пропишет его в `assets/site.js` (константа `LEAD_ENDPOINT`) и задеплоит.

## Проверка
Открой mentio.agency, введи домен в сканер внизу страницы, оставь контакт —
сообщение должно прийти в Telegram в течение секунды.

## Формат сообщения
🔥 Новый лид с mentio.agency
🌐 Сайт: example.com
📬 Контакт: name@mail.com
📊 AI Visibility Score: 57/100 (если лид из теста)
🏷 Источник: сканер сайта / тест AI Visibility
🌍 Язык страницы: uk (/ua/)
