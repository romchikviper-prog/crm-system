# CRM System

[![CI](https://github.com/romchikviper-prog/crm-system/actions/workflows/ci.yml/badge.svg)](https://github.com/romchikviper-prog/crm-system/actions/workflows/ci.yml)

CRM-система для автоматизації роботи з клієнтами та контролю замовлень.

## Про проєкт

Система призначена для ведення бази клієнтів, обліку замовлень, контролю їхніх
статусів, роботи з каталогом товарів, формування аналітики та надсилання
повідомлень клієнтам.

Проєкт розвивається поетапно. У лабораторній роботі №3 створено репозиторій,
налаштовано середовище розробки, закладено базову структуру та реалізовано
перший модуль — облік клієнтів.

## Технології

| Компонент | Рішення |
|---|---|
| Мова | Python 3.13 |
| Вебфреймворк | FastAPI |
| ORM | SQLAlchemy 2.0 |
| База даних | PostgreSQL 16 |
| Контейнеризація | Docker Compose |
| Тести | pytest |
| Лінтер | Ruff |

## Структура проєкту

```text
crm-system/
├── app/
│   ├── api/              # маршрутизація HTTP-запитів
│   ├── core/             # конфігурація, логування, обробка помилок
│   ├── db/               # підключення до бази даних
│   └── modules/          # бізнес-модулі системи
│       ├── auth/
│       ├── customers/    # реалізований модуль
│       ├── orders/
│       ├── products/
│       ├── analytics/
│       └── notifications/
├── docs/                 # проєктна документація
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
.venv\Scripts\activate
pip install -r requirements-dev.txt
```

### 5. Запуск API-сервера

```bash
uvicorn app.main:app --reload
```

Сервіс доступний за адресою http://localhost:8000, інтерактивна документація —
http://localhost:8000/docs.

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
pytest --cov=app --cov-report=term-missing
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

## Робота з гілками

- `main` — стабільна версія;
- `develop` — інтеграційна гілка;
- `feature/*` — окремі функціональні зміни.

Правила комітів і pull request описано в [CONTRIBUTING.md](CONTRIBUTING.md).

## Автор

Гольда Роман Павлович, група 7.F3.26
