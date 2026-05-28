# Tutor Scheduler

Веб-приложение для автоматизации работы репетитора: расписание, ученики, аналитика.

## Быстрый старт

```bash
cd tutor_scheduler
bash start.sh
```

Откройте http://localhost:8000 в браузере.

## Стек

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, SQLite
- **Auth**: JWT (python-jose), bcrypt (passlib)
- **Frontend**: Чистый HTML/JS/CSS (SPA, без фреймворков)

## Структура

```
tutor_scheduler/
├── app/
│   ├── main.py              # FastAPI приложение
│   ├── core/
│   │   ├── database.py      # SQLAlchemy + SQLite
│   │   └── security.py      # JWT, bcrypt
│   ├── models/
│   │   └── models.py        # User, Student, Lesson
│   ├── schemas/
│   │   └── schemas.py       # Pydantic схемы
│   └── routers/
│       ├── auth.py          # POST /auth/register, /auth/login
│       ├── students.py      # CRUD /students/
│       ├── lessons.py       # CRUD /lessons/
│       └── stats.py         # GET /stats/summary
├── frontend/
│   └── index.html           # Одностраничное приложение
├── requirements.txt
├── start.sh
└── README.md
```

## API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| POST | /auth/register | Регистрация |
| POST | /auth/login | Вход (OAuth2 form) |
| GET | /students/ | Список учеников |
| POST | /students/ | Создать ученика |
| PUT | /students/{id} | Обновить ученика |
| DELETE | /students/{id} | Удалить ученика |
| GET | /lessons/ | Список уроков (фильтры: start, end, student_id) |
| POST | /lessons/ | Создать урок |
| PUT | /lessons/{id} | Обновить урок |
| DELETE | /lessons/{id} | Удалить урок |
| GET | /stats/summary | Аналитика (period: week/month/year/all) |

## Интерактивная документация

После запуска: http://localhost:8000/docs (Swagger UI)

## Переход на PostgreSQL

В `app/core/database.py` замените:
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/tutor_scheduler"
```
И добавьте `psycopg2-binary` в requirements.txt.

## Переменные окружения (для продакшена)

Создайте `.env` и обновите `SECRET_KEY` в `app/core/security.py`:
```
SECRET_KEY=ваш-секретный-ключ-минимум-32-символа
```
