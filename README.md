# Личный кабинет агента недвижимости

**Веб-приложение для управления объявлениями о недвижимости с аналитикой и фильтрацией**


## Возможности

- Авторизация и регистрация агентов
- Создание/редактирование/удаление объявлений
- Фильтрация объявлений по параметрам
- Аналитика: количество объявлений, средняя цена, топ городов
- Удобное управление недвижимостью

## Быстрый старт

### 1. Клонирование репозитория

```bash
git clone https://github.com/ваш-username/real-estate-agent.git
cd AGent
```

### 2. Настройка окружения

Создайте и активируйте виртуальное окружение:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Запуск приложения

```bash
python app.py
```

Приложение будет доступно по адресу: [http://localhost:5000](http://localhost:5000)


## Зависимости

- Python 3.8+
- Flask 2.2.5
- Flask-SQLAlchemy 3.0.3
- Flask-Login 0.6.2
- SQLAlchemy 1.4.46
- Werkzeug 2.2.3

## Структура проекта

```
real-estate-agent/
├── app.py              # Основное приложение
├── extensions.py       # Инициализация расширений
├── models.py           # Модели базы данных
├── requirements.txt    # Зависимости
├── static/             # Статические файлы
│   └── style.css       # Стили CSS
└── templates/          # Шаблоны
    ├── base.html       # Базовый шаблон
    ├── login.html      # Страница входа
    ├── register.html   # Страница регистрации
    ├── dashboard.html  # Личный кабинет
    ├── listings.html   # Список объявлений
    └── edit_listing.html # Редактирование объявлений
```

## Лицензия

MIT License

---

**Автор**: Горобцов Андрей Александрович
**Email**: AndreyAG2142@gmail.com  
**Версия**: 1.0.0