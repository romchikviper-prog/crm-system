# CRM System

[![CI](https://github.com/romchikviper-prog/crm-system/actions/workflows/ci.yml/badge.svg)](https://github.com/romchikviper-prog/crm-system/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/romchikviper-prog/crm-system?label=release)](https://github.com/romchikviper-prog/crm-system/releases)

CRM-система для автоматизації роботи з клієнтами та контролю замовлень.

## Про проєкт

Система призначена для ведення бази клієнтів, обліку замовлень, контролю їхніх
статусів, роботи з каталогом товарів, формування аналітики та надсилання
повідомлень клієнтам.

Поточний реліз — **1.0.0**. Він охоплює реалізований обсяг: REST API обліку
клієнтів, службові маршрути, централізовану обробку помилок, логування,
автоматичні тести, CI/CD і Docker-образ. Повний MVP CRM (модулі `auth`,
`products`, `orders`, `analytics`, `notifications`) ще не завершений; відкриті
завдання відстежуються в GitHub Issues.

## Реліз 1.0.0

| Артефакт | Розташування |
|---|---|
| GitHub Release | https://github.com/romchikviper-prog/crm-system/releases/tag/v1.0.0 |
| Docker-образ | `ghcr.io/romchikviper-prog/crm-system:1.0.0` |
| Журнал змін | [CHANGELOG.md](CHANGELOG.md) |
| Інструкція з розгортання | [docs/deployment.md](docs/deployment.md) |
| План підтримки | [docs/support.md](docs/support.md) |

Завантаження опублікованого образу:

```bash
docker pull ghcr.io/romchikviper-prog/crm-system:1.0.0
```

Повна послідовність розгортання, оновлення та відкату наведена в
[docs/deployment.md](docs/deployment.md).

## Технології

| Компонент | Рішення |
|---|---|
| Мова | Python 3.13 |
| Вебфреймворк | FastAPI |
| ORM | SQLAlchemy 2.0 |
| База даних | PostgreSQL 16 |
| Контейнеризація | Docker, Docker Compose |
| Тести | pytest, Postman/Newman |
| Лінтер | Ruff |
| CI/CD | GitHub Actions, GitHub Container Registry |

## Структура проєкту

```text
crm-system/
├── app/
│   ├── api/              # маршрутизація HTTP-запитів
│   ├── core/             # конфігурація, логування, обробка помилок
│   ├── db/               # підключення до бази даних
│   └── modules/          # бізнес-модулі системи
│       ├── auth/         # заплановано
│       ├── customers/    # реалізовано
│       ├── orders/       # заплановано
│       ├── products/     # заплановано
│       ├── analytics/    # заплановано
│       └── notifications/ # заплановано
├── docs/                 # проєктна та супровідна документація
├── postman/              # колекція та середовище Newman
├── tests/                # тести
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## Швидкий старт

### 1. Клонування репозиторію

```bash
git clone https://github.com/romchikviper-prog/crm-system.git
cd crm-system
git checkout v1.0.0
```

### 2. Налаштування змінних середовища

```bash
cp .env.example .env
```

### 3. Запуск бази даних

```bash
docker compose up -d db
```

### 4. Встановлення залежностей

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 5. Запуск API-сервера

```bash
uvicorn app.main:app --reload
```

Сервіс доступний за адресою http://localhost:8000, інтерактивна документація —
http://localhost:8000/docs.

Повний стек у контейнерах запускається командою:

```bash
docker compose up -d --build
```

## API

| Метод | Шлях | Призначення |
|---|---|---|
| GET | `/` | Інформація про сервіс |
| GET | `/api/v1/health` | Перевірка стану сервісу та бази даних |
| GET | `/api/v1/customers` | Перелік клієнтів |
| POST | `/api/v1/customers` | Створення клієнта |
| GET | `/api/v1/customers/{id}` | Отримання клієнта за ідентифікатором |

Приклад створення клієнта:

```bash
curl -X POST http://localhost:8000/api/v1/customers \
  -H "Content-Type: application/json" \
  -d "{\"full_name\":\"Іван Петренко\",\"email\":\"ivan@example.com\"}"
```

## Перевірка якості коду

```bash
ruff check .
ruff format --check .
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
```

## Автоматизовані тести API

Функціональні та регресійні тести API виконуються колекцією Postman через
Newman. Для запуску API має бути доступним на `http://127.0.0.1:8000`.

```bash
newman run postman/CRM-System.postman_collection.json \
  -e postman/CRM-System.postman_environment.json \
  -n 10 -r cli,json,htmlextra
```

Детальніше — у [postman/README.md](postman/README.md).

## Безперервна інтеграція та розгортання

Кожен push і pull request до гілок `main` та `develop` автоматично перевіряється
в GitHub Actions. Пайплайн складається з таких етапів:

| Етап | Що виконується |
|---|---|
| Якість коду | `ruff check .`, `ruff format --check .` |
| Тести | `pytest` із покриттям, поріг 80% |
| Інтеграція | API на PostgreSQL 16, перевірка стану та колекція Newman |
| Збірка | `docker build` образу застосунку |
| Публікація | Docker-образ у GitHub Container Registry за тегом `v*` |

Конфігурація — [.github/workflows/ci.yml](.github/workflows/ci.yml) і
[.github/workflows/cd.yml](.github/workflows/cd.yml). Повний опис процесів —
у [docs/ci-cd.md](docs/ci-cd.md).

## Підтримка та оновлення

- Зворотний зв’язок збирається через GitHub Issues (помилки, покращення,
  питання).
- Версіонування — Semantic Versioning; зміни фіксуються в
  [CHANGELOG.md](CHANGELOG.md).
- Порядок виправлення дефектів, строки реакції, регресійне тестування та
  чек-лист релізу описані в [docs/support.md](docs/support.md).
- Базовий моніторинг — журнали API з `X-Request-ID`, маршрут
  `/api/v1/health` і статус GitHub Actions.

## Обмеження релізу 1.0.0

- Реалізовано лише модуль `customers`; інші бізнес-модулі заплановані.
- Відсутні автентифікація й авторизація, тому API не можна відкривати в
  інтернет без зворотного проксі, VPN або іншого захисту.
- Перелік клієнтів повертається без пагінації; `PATCH` і `DELETE` не
  реалізовані.
- Схема бази створюється через `create_all`; міграції Alembic заплановані.

## Робота з гілками

- `main` — стабільна версія;
- `develop` — інтеграційна гілка;
- `feature/*` — окремі функціональні зміни;
- `release/*` — підготовка релізу.

Правила комітів і pull request описано в [CONTRIBUTING.md](CONTRIBUTING.md).

## Автор

Гольда Роман Павлович, група 7.F3.26
