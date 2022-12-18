**О проекте:**
----------

Проект YaMDb собирает отзывы пользователей на различные произведения (фильмы, книги и т.п.).


**Cсылки к проекту**
----------

Адрес проекта: http://51.250.18.156

Документация по API: http://51.250.18.156/redoc/


**Workflow status badge:**
----------

[![Status badge](https://github.com/ushakov-ya2016/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)]()


**Запуск проекта локально по адресу 127.0.0.1:** 
---------- 

1. Клонировать репозиторий и перейти в него в командной строке: 

git clone https://https://github.com/ushakov-ya2016/yamdb_final

2. Перейти в директорию проекта, в которой расположен файл docker-compose.yaml:

cd yamdb_final
cd infra

3. Развернуть проект:

docker-compose up

4. После успешного разворачивания проекта, создать дополнительное окно терминала и выполнить миграции:

docker-compose exec web python manage.py migrate

5. Создать суперпользователя для доступа к админке http://127.0.0.1/admin/:

docker-compose exec web python manage.py createsuperuser

6. Собрать статику:

docker-compose exec web python manage.py collectstatic --no-input

7. Документация к API проекта будет доступна по адресу http://127.0.0.1/redoc/


**Шаблон наполнения env-файла** 
----------

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql 
DB_NAME=postgres # имя базы данных 
POSTGRES_USER=user # логин для подключения к базе данных 
POSTGRES_PASSWORD=password # пароль для подключения к БД 
DB_HOST=db # название сервиса (контейнера) 
DB_PORT=5432 # порт для подключения к БД 
SECRET_KEY='1231223123123' # секретный ключ проекта Django


**Автор**
----------

Ушаков Александр, Яндекс.Практикум, когорта № 40
