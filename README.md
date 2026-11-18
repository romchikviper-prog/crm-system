# CRM System

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
pytest
```

## Робота з гілками

- `main` — стабільна версія;
- `develop` — інтеграційна гілка;
- `feature/*` — окремі функціональні зміни.

Правила комітів і pull request описано в [CONTRIBUTING.md](CONTRIBUTING.md).

## Автор

Гольда Роман Павлович, група 7.F3.26
