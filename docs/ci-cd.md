# Безперервна інтеграція та розгортання CRM System

Документ описує автоматизацію життєвого циклу проєкту засобами GitHub Actions:
перевірку якості коду, тестування, інтеграційну перевірку API з PostgreSQL,
збірку Docker-образу та публікацію образу в GitHub Container Registry.

## Призначення

Пайплайн запускається автоматично та не потребує ручних команд розробника.
Його мета — не допустити потрапляння до `main` і `develop` змін, які порушують
стиль коду, форматують файли інакше за домовлений стандарт, ламають тести або
порушують взаємодію API з базою даних.

## Тригери

| Подія | Гілки | Workflow |
|---|---|---|
| `push` | `main`, `develop` | CI |
| `pull_request` | `main`, `develop` | CI |
| Ручний запуск (`workflow_dispatch`) | будь-яка | CI, CD |
| `push` тега `v*` | — | CD |

Для кожного ref створюється окрема група `concurrency`; новий запуск скасовує
попередній незавершений запуск для того самого ref.

## Схема пайплайна

```mermaid
flowchart LR
    A[push / pull_request] --> B[Якість коду]
    A --> C[Тести]
    B --> D[Інтеграція]
    C --> D
    B --> E[Збірка]
    C --> E
    F[тег v*] --> G[CD: публікація образу]
```

## Етапи CI

Конфігурація: [`.github/workflows/ci.yml`](../.github/workflows/ci.yml).

| Етап | Команди | Залежності | Результат |
|---|---|---|---|
| Якість коду | `ruff check .`, `ruff format --check .` | — | Перевірений стиль і форматування |
| Тести | `pytest --cov=app --cov-report=term-missing --cov-report=xml --cov-fail-under=80` | — | Звіт `coverage-xml` |
| Інтеграція | `uvicorn`, `curl /api/v1/health`, `newman run ... -n 3` | Якість коду, тести | Звіт `newman-report` |
| Збірка | `docker build --tag crm-system:<sha> .` | Якість коду, тести | Docker-образ |

Етапи «Якість коду» і «Тести» виконуються паралельно. «Інтеграція» та
«Збірка» стартують лише після їхнього успішного завершення.

### Інтеграційна перевірка

Етап «Інтеграція» піднімає службовий контейнер `postgres:16-alpine` з базою
`crm`, запускає застосунок командою
`uvicorn app.main:app --host 127.0.0.1 --port 8000` зі змінною
`DATABASE_URL=postgresql+psycopg://crm:crm@127.0.0.1:5432/crm` і чекає
відповіді `/api/v1/health`. Після цього виконується колекція Postman із трьома
ітераціями. Перевіряються створення клієнта, читання за ідентифікатором,
перелік, конфлікт унікальної пошти, 404, 422, кореневий маршрут і OpenAPI.

Така перевірка охоплює весь ланцюжок «HTTP-маршрут → сервіс → репозиторій →
SQLAlchemy → PostgreSQL», а не лише окремі функції.

## Етап CD

Конфігурація: [`.github/workflows/cd.yml`](../.github/workflows/cd.yml).

Workflow CD запускається після push тега `v*` або вручну. Він:

1. налаштовує Docker Buildx;
2. виконує вхід до `ghcr.io` з `GITHUB_TOKEN`;
3. формує теги образу: тег релізу, `sha-<короткий хеш>` і `latest`;
4. збирає образ і публікує його в
   `ghcr.io/romchikviper-prog/crm-system`;
5. використовує кеш GitHub Actions для повторних збірок.

Опублікований образ є готовим артефактом розгортання. Розгортання на конкретний
хостинг у проєкті не налаштоване, оскільки цільове середовище не визначене.

## Локальне відтворення перевірок

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements-dev.txt

ruff check .
ruff format --check .
pytest --cov=app --cov-report=term-missing

uvicorn app.main:app --host 127.0.0.1 --port 8000
newman run postman/CRM-System.postman_collection.json \
  -e postman/CRM-System.postman_environment.json \
  -n 3
```

Для перевірки на PostgreSQL потрібно задати `DATABASE_URL` перед запуском
`uvicorn`; для швидкої локальної перевірки достатньо SQLite.

## Результати

Результати запусків наведено в таблиці.

| Запуск | Подія | Статус | Тривалість |
|---|---|---|---|
| CI №1 (pull request #14) | `pull_request` | успішно | 1 хв 07 с |
| CI №2 (develop після злиття) | `push` | успішно | — |
| CD №1 (ручний запуск) | `workflow_dispatch` | успішно | — |

## Обмеження

- Docker Desktop на локальному комп'ютері не встановлено, тому збірка образу та
  контейнерна інтеграція виконуються на GitHub runner.
- Розгортання на зовнішній хостинг не виконується: CD публікує образ у GHCR.
- Тести `pytest` використовують SQLite; взаємодія з PostgreSQL перевіряється
  окремим інтеграційним етапом через Newman.
