Запуск базы в докере, а приложения без докера:
- docker-compose up pg
- flask run

Запуск в докере при дебаге:
- docker-compose -f docker-compose.debug.yml up --build
- Присоединить дебаг listener на порт 5678
При этом автоматически применяются миграции и заполняются тестовые данные.
  
Запуск в докере при продакшене(промежуточный вариант только через gunicorn):
- docker-compose up --build

Для ручного применения миграция:
- flask db upgrade

А также заполнить данными:
- flask fill-db

В процессе миграций автоматически создается админ:
- name=admin
- email=admin@google.com
- password=123