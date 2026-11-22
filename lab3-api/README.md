# Лабораторная работа 3: Python API в контейнере

## Описание
Доработанное API каталога учебных материалов с фильтрацией по теме и сводкой.
В каталоге 7 записей: 3 по linux, 3 по podman, 1 по python.

## Команды сборки и запуска
### Запуск контейнера
docker run -d --name lab-api-v2 -p 127.0.0.1:8102:8000 localhost/lab-api:v2
### Остановка контейнера
docker stop lab-api-v2
### Удаление контейнера (при конфликте имени)
docker rm lab-api-v2
## Фактические HTTP-ответы из контейнера
###  1. GET /api/items?topic=podman (Статус: 200 OK)
{
  "items": [
    {"id": 4, "title": "Введение в контейнеры", "topic": "podman"},
    {"id": 5, "title": "Сборка образов", "topic": "podman"},
    {"id": 7, "title": "Продвинутый Podman", "topic": "podman"}
  ]
}
### 2. GET /api/items?topic=unknown (Статус: 200 OK)
{
  "items": []
}
### 3. GET /api/summary (Статус: 200 OK)
{
  "total": 7,
  "by_topic": {
    "linux": 3,
    "podman": 3,
    "python": 1
  }
}

### Сборка образа
docker build -f Containerfile -t localhost/lab-api:v2 .