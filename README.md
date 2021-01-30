[![Python version](https://img.shields.io/badge/Python-3.7.5-green)](https://www.python.org/)
[![Django version](https://img.shields.io/badge/Django-3.1.5-green)](https://docs.djangoproject.com/en/3.0/)

# My_site - Моей мини проект для оптимизации рутинной работы

## Main design goals

- Мини блог
- Сайт для повторения английских слов с ранжированием
- Сайт подсчет калорий
- Бот для напоминаний

## status
- рання версия

## setting up a project

- в settings.py настраиваем подключения к БД
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '***',
        'USER': '***',
        'PASSWORD': '***',
        'HOST': '***',
        'PORT': '***',
    }
}
```
- в settings.py настраиваем подключения к почте
```python
EMAIL_HOST = '***'
EMAIL_HOST_USER = '***'
EMAIL_HOST_PASSWORD = '***'
EMAIL_PORT = '***'
```