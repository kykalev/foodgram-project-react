FoodGramm «Продуктовый помощник»
=====

Работающий проект
----------

* адрес http://84.252.143.34/
* почта admin@admin.ru
* пароль admin

Описание
----------

На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Стек технологий
----------
* Python 3.9
* Django 4.1
* Django REST Framework
* React
* PostgreSQL
* Docker
* DockerHub
* Nginx
* Gunicorn

Наполнение ```.env``` файла.
----------

* SECRET_KEY=vash_secret_django - секретный ключ Django;
* DB_ENGINE=django.db.backends.postgresql - работаем с бд postgresql
* DB_NAME=postgres - имя базы данных
* POSTGRES_USER=postgres - логин для подключения к БД;
* POSTGRES_PASSWORD=postgres - пароль для подключения к БД;
* DB_HOST=db - название сервиса (контейнера);
* DB_PORT=5432 - порт для подключения к БД;


Установка проекта из репозитория
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```bash
git clone git@github.com:kykalev/foodgram-project-react.git

cd Foodgramm
```
2. Cоздать и открыть файл ```.env``` с переменными окружения в папке infra:
```bash 
cd infra

touch .env
```
3. Заполнить ```.env``` файл с переменными окружения:
4. Установка и запуск приложения в контейнерах (контейнер backend загружактся из DockerHub):
```bash 
docker-compose up -d
```
5. Запуск миграций, сбор статики, заполнение БД ингредиентами и создание admin:
```bash 
docker-compose exec backend python manage.py migrate

docker-compose exec backend python manage.py collectstatic --no-input 

docker-compose exec backend python manage.py csv_to_db ingredients.csv

docker-compose exec backend python manage.py createsuperuser
```
