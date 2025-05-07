# QRKot

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![SQLAlchemy](https://img.shields.io/badge/-SQLAlchemy-464646?style=flat&logo=SQLAlchemy)](https://www.sqlalchemy.org/)
[![FastAPI](https://img.shields.io/badge/-FastAPI-464646?style=flat&logo=FastAPI)](https://fastapi.tiangolo.com/)
[![Alembic](https://img.shields.io/badge/-Alembic-464646?style=flat&logo=alembic)](https://alembic.sqlalchemy.org/)
[![Pydantic](https://img.shields.io/badge/-Pydantic-464646?style=flat&logo=pydantic)](https://docs.pydantic.dev/)

## Описание
Проект QRKot — это благотворительный фонд поддержки котов. Фонд собирает пожертвования на любые цели, связанные с поддержкой кошачьей популяции. Сервис позволяет создавать проекты по сбору средств и делать пожертвования. Пожертвования автоматически распределяются между проектами.

Документация API: **"openapi.json"**

### Как запустить проект:
Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Savva17/cat_charity_fund.git
```

```
cd cat_charity_fund
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

## Запуск проекта

```
uvicorn app.main:app --reload
```
Документация Swagger по адресу:
```
http://127.0.0.1:8000/docs
```
Документация Redoc по адресу:
```
http://127.0.0.1:8000/redoc
```

Автор проекта: Морозов Савва

Профиль автора на GitHub:
- **GitHub**: [Профиль Савва Морозов](https://github.com/Savva17)