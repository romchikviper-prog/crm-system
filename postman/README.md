# Тести якості API (Postman + Newman)

У папці розміщено автоматизовану колекцію перевірки REST API CRM System.

## Склад

| Файл | Призначення |
|---|---|
| `CRM-System.postman_collection.json` | 10 запитів і 44 assertions на ітерацію |
| `CRM-System.postman_environment.json` | Локальне середовище (`baseUrl = http://127.0.0.1:8000`) |

## Що перевіряється

- стан сервісу та доступність бази даних;
- створення клієнта, отримання за ідентифікатором, перелік клієнтів;
- конфлікт унікальної електронної пошти (409);
- відсутній ресурс (404);
- валідація тіла запиту та параметра шляху (422);
- єдина структура помилок `error.code`, `error.message`, `error.request_id`;
- заголовок `X-Request-ID`;
- OpenAPI-документація;
- час відповіді (поріг 1000 мс).

## Запуск

1. Запустити API:

   ```bash
   uvicorn app.main:app --host 127.0.0.1 --port 8000
   ```

2. Встановити Newman:

   ```bash
   npm install -g newman newman-reporter-htmlextra
   ```

3. Виконати колекцію (10 ітерацій):

   ```bash
   newman run postman/CRM-System.postman_collection.json \
     -e postman/CRM-System.postman_environment.json \
     -n 10 -r cli,json,htmlextra
   ```

Для іншого середовища достатньо змінити `baseUrl` у файлі середовища
або передати його через `--env-var "baseUrl=http://host:port"`.

## Результат

Останній запуск: 10 ітерацій, 100 запитів, 440 assertions, 0 помилок,
середній час відповіді 3,65 мс, p95 — 7 мс. Детальні результати —
у `qa/reports/newman-summary.md`.
