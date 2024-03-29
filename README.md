# Опросный сервис на базе Django

Это веб-приложение создано для проведения опросов с учетом пользователя и динамическим отображением вопросов в зависимости от предыдущих ответов.

## Функциональность

1.  **Создание и редактирование опросов и вопросов через админку:**
    -   Войдите в административный интерфейс Django для создания и редактирования опросов и вопросов.
2.  **Веб-интерфейс для пользователей:**
    -   Пользователи могут проходить опросы и отвечать на вопросы через удобный веб-интерфейс.
3.  **Сохранение ответов пользователей:**
    -   Ответы пользователей сохраняются в связке с соответствующими опросами.
4.  **Динамическое отображение вопросов:**
    -   Логика определения, какие вопросы показывать или скрывать, зависит от предыдущих ответов пользователя.
5.  **Вывод результатов опросов:**
    -   После завершения опроса доступны результаты, включая статистику ответов на каждый вопрос.

## Реализация

-   Используется Django для создания веб-приложения.
-   Минимальное количество SQL-запросов без использования ORM.

## Как запустить проект:

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```