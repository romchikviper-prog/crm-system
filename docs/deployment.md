# Розгортання CRM System 1.0.0

Інструкція призначена для адміністраторів, які розгортають CRM System на
власному сервері або робочій станції. Реліз 1.0.0 постачається як вихідний
код, Docker-образ і супровідна документація.

## 1. Склад релізу

| Артефакт | Розташування |
|---|---|
| Вихідний код | GitHub, тег `v1.0.0` |
| Docker-образ | `ghcr.io/romchikviper-prog/crm-system:v1.0.0` |
| Журнал змін | `CHANGELOG.md` |
| API-документація | `http://<host>:8000/docs`, `http://<host>:8000/openapi.json` |
| План підтримки | `docs/support.md` |

## 2. Вимоги

- Docker Engine 24+ або Docker Desktop із Docker Compose v2.
- 2 ГБ оперативної пам’яті та 1 ГБ вільного дискового простору.
- Вільні порти `8000` (API) і `5432` (PostgreSQL) або інші значення в
  конфігурації.
- Для локального режиму без Docker: Python 3.13 і PostgreSQL 16.

## 3. Варіант A. Docker Compose із вихідного коду

Цей режим зручний для демонстрації та повторюваного розгортання.

```bash
git clone https://github.com/romchikviper-prog/crm-system.git
cd crm-system
git checkout v1.0.0
cp .env.example .env
docker compose up -d --build
```

Перевірка стану контейнерів:

```bash
docker compose ps
```

Обидва контейнери (`crm-db` і `crm-api`) мають бути в стані `running`, а
`crm-db` — `healthy`. API буде доступний на порту `8000`.

## 4. Варіант B. Опублікований образ GHCR

Цей режим не потребує клонування репозиторію. Спочатку створіть мережу та
том для даних:

```bash
docker network create crm-net
docker volume create crm_pgdata
```

Запустіть PostgreSQL 16. Замініть `<password>` на власний пароль:

```bash
docker run -d --name crm-db --network crm-net --restart unless-stopped \
  -e POSTGRES_DB=crm \
  -e POSTGRES_USER=crm \
  -e POSTGRES_PASSWORD='<password>' \
  -v crm_pgdata:/var/lib/postgresql/data \
  --health-cmd "pg_isready -U crm -d crm" \
  --health-interval 5s \
  --health-timeout 5s \
  --health-retries 10 \
  postgres:16-alpine
```

Дочекайтеся готовності бази:

```bash
until docker exec crm-db pg_isready -U crm -d crm; do sleep 1; done
```

Запустіть API з опублікованого образу:

```bash
docker run -d --name crm-api --network crm-net --restart unless-stopped \
  -p 127.0.0.1:8000:8000 \
  -e DATABASE_URL='postgresql+psycopg://crm:<password>@crm-db:5432/crm' \
  -e ENVIRONMENT=production \
  -e LOG_LEVEL=INFO \
  ghcr.io/romchikviper-prog/crm-system:v1.0.0
```

Якщо пароль містить символи `@`, `:`, `/` або `#`, його потрібно
URL-кодувати в `DATABASE_URL`.

Прив’язка `127.0.0.1:8000:8000` залишає API доступним лише з локальної
машини. Для доступу із зовнішньої мережі використовуйте зворотний проксі з
TLS та автентифікацією (див. розділ 9).

## 5. Варіант C. Локальний запуск без Docker

```bash
git clone https://github.com/romchikviper-prog/crm-system.git
cd crm-system
git checkout v1.0.0
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

У `.env` задайте підключення до PostgreSQL 16, наприклад:

```text
DATABASE_URL=postgresql+psycopg://crm:crm@localhost:5432/crm
ENVIRONMENT=production
LOG_LEVEL=INFO
```

Запуск API:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## 6. Змінні середовища

| Змінна | Призначення | Приклад |
|---|---|---|
| `DATABASE_URL` | Рядок підключення до PostgreSQL | `postgresql+psycopg://crm:crm@crm-db:5432/crm` |
| `ENVIRONMENT` | Назва середовища в логах і health | `production` |
| `LOG_LEVEL` | Рівень журналювання | `INFO`, `WARNING`, `ERROR` |
| `DEBUG` | Режим налагодження | `false` |

Файл `.env` не додається до репозиторію. У репозиторії є лише
`.env.example`.

## 7. Перевірка після запуску

1. Кореневий маршрут:

   ```bash
   curl http://localhost:8000/
   ```

   Очікувана відповідь містить назву сервісу, версію `1.0.0` і шлях до
   документації.

2. Стан сервісу та бази даних:

   ```bash
   curl http://localhost:8000/api/v1/health
   ```

   Очікувана відповідь:

   ```json
   {
     "status": "ok",
     "service": "CRM System",
     "version": "1.0.0",
     "environment": "production",
     "database": "ok"
   }
   ```

3. Інтерактивна документація: `http://localhost:8000/docs`.

4. Журнал API:

   ```bash
   docker logs --tail 50 crm-api
   ```

## 8. Оновлення та відкат

Порядок оновлення на прикладі версії `1.0.1`:

1. Зробіть резервну копію бази (розділ 10).
2. Завантажте новий образ:

   ```bash
   docker pull ghcr.io/romchikviper-prog/crm-system:v1.0.1
   ```

3. Зупиніть і видаліть контейнер API, не видаляючи том даних:

   ```bash
   docker stop crm-api
   docker rm crm-api
   ```

4. Запустіть контейнер із новим тегом, як у розділі 4.
5. Перевірте `/api/v1/health` і журнал.
6. Перегляньте `CHANGELOG.md` та release notes.

Для відкату виконайте ті самі кроки з попереднім тегом, наприклад
`1.0.0`. Дані в томі `crm_pgdata` зберігаються між версіями.

## 9. Безпека

У релізі 1.0.0 **відсутня автентифікація**. Це навчальний реліз, тому:

- не публікуйте порт `8000` у відкритий інтернет;
- використовуйте прив’язку до `127.0.0.1`, VPN або зворотний проксі
  (Nginx, Traefik) із TLS та автентифікацією;
- замініть тестовий пароль PostgreSQL на складний і зберігайте його поза
  репозиторієм;
- обмежте доступ до порту `5432` лише мережею контейнерів;
- регулярно оновлюйте базовий образ `postgres:16-alpine` і залежності
  Python.

## 10. Резервне копіювання та відновлення

Створення резервної копії:

```bash
docker exec crm-db pg_dump -U crm -d crm > crm_backup_$(date +%F).sql
```

Відновлення:

```bash
cat crm_backup_2026-11-21.sql | docker exec -i crm-db psql -U crm -d crm
```

Резервні копії слід зберігати поза сервером і перевіряти відновлення на
тестовому середовищі.

## 11. Діагностика

| Симптом | Що перевірити |
|---|---|
| `crm-api` постійно перезапускається | `docker logs crm-api`; правильність `DATABASE_URL`; готовність `crm-db` |
| `/api/v1/health` повертає `database: error` | доступність PostgreSQL, пароль, назву бази |
| Порт `8000` зайнятий | змініть публікацію порту або зупиніть інший процес |
| Помилка 500 | знайдіть `request_id` у відповіді та в журналі API |
| Образ не завантажується | перевірте доступ до `ghcr.io` і тег `v1.0.0` |

Для звернення до підтримки зберіть версію, середовище, кроки відтворення,
очікуваний і фактичний результат, логи та `request_id`. Порядок описано в
`docs/support.md`.
