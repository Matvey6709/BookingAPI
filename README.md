# 📅 Bookings API

REST API для управления бронированиями отелей, реализованный с использованием FastAPI, Celery, PostgreSQL, Redis и Grafana.

---

## 🚀 Технологии

- **FastAPI** — современный веб-фреймворк для создания API на Python  
- **Celery** — система для обработки фоновых задач  
- **PostgreSQL** — реляционная база данных  
- **Redis** — брокер сообщений для Celery и кеш  
- **Grafana** — мониторинг и визуализация метрик  
- **Админка** — для управления сущностями и бронированиями  

---

## 📋 Описание проекта

API предназначено для управления пользователями, отелями, комнатами и бронированиями.  
Поддерживаются регистрация, аутентификация, авторизация, а также обработка фоновых задач через Celery.  
Для мониторинга работы сервиса используется Grafana.  

---

## 🗂 Структура базы данных

| Таблица   | Поля                                                                                              |
|-----------|-------------------------------------------------------------------------------------------------|
| **Users** | `id (int)`, `email (varchar)`, `hashed_password (varchar)`                                      |
| **Hotels**| `id (int)`, `name (varchar)`, `location (varchar)`, `services (json list)`, `rooms_quantity (int)`, `image_id (int)` |
| **Rooms** | `id (int)`, `hotel_id (int)`, `name (varchar)`, `description (varchar)`, `price (int)`, `services (json list)`, `quantity (int)`, `image_id (int)` |
| **Bookings** | `id (int)`, `room_id (int)`, `user_id (int)`, `date_from (date)`, `date_to (date)`, `price (int)`, `total_cost (int)`, `total_days (int)` |

---

## 🛠 Установка и запуск

### Клонирование репозитория

```bash
git clone https://github.com/Matvey6709/BookingAPI.git
cd repo-name
```
## Настройка переменных окружения

Создайте файл .env на основе примера .env.example и укажите необходимые значения:

```bash
cp .env.example .env
```

## Запуск с помощью Docker

```bash
docker-compose up --build
```
