**О проекте:**
----------

Проект YaMDb собирает отзывы пользователей на различные произведения (фильмы, книги и т.п.).


**Cсылки к проекту**
----------

Адрес проекта: http://51.250.18.156

Документация по API: http://51.250.18.156/redoc/

Вход в панель администрирования: http://51.250.18.156/admin/


**Workflow status badge:**
----------

[![Status badge](https://github.com/ushakov-ya2016/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)]()


**Как запустить проект:**
----------

1. Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://https://github.com/ushakov-ya2016/yamdb_final
```
```
cd yamdb_final
```
2. Cоздать и активировать виртуальное окружение:
```
python -m venv venv
```
```
source venv/bin/activate
```
3. Обновите pip до последней версии:
```
python -m pip install --upgrade pip command
```
4. Установите необходимые зависимости:
```
cd api_yamdb
pip install -r requirements.txt
```
5. Перейдите в директорию infra и разверните проект:
```
cd ..
cd infra
docker-compose up
```
6. После успешного разворачивания проекта, создайте дополнительное окно терминала и выполните миграции:
```
docker-compose exec web python manage.py migrate
```
7. Создайте суперпользователя для доступа к админке:
```
docker-compose exec web python manage.py createsuperuser
```
8. Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input
```

**Шаблон наполнения env-файла**

DB_ENGINE=django.db.backends.postgresql # указываем, что работаем с postgresql
DB_NAME=postgres # имя базы данных
POSTGRES_USER=user # логин для подключения к базе данных
POSTGRES_PASSWORD=password # пароль для подключения к БД
DB_HOST=db # название сервиса (контейнера)
DB_PORT=5432 # порт для подключения к БД
SECRET_KEY='1231223123123' # секретный ключ проекта Django

**Автор**

Ушаков Александр, Яндекс.Практикум, когорта № 40
