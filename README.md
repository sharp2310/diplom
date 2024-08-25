# "Образовательные модули"

"Образовательные модули" - приложение для обучения 
посредством модулей, которые принадлежат образовательному порталу.
Любой пользователь может создавать свои образовательные модули, загружать
их в систему и редактировать их. Так же, любой пользователь может подписываться
на образовательные модули и просматривать их. Понравившиеся модули можно отмечать "лайками".
Если пользователь подписан на модуль, то он будет получать уведомления о изменениях в образовательных модулях.

## Установка и запуск проекта:

* клонировать репозиторий: git clone https://github.com/sharp2310/diplom
* установить виртуальную среду: python -m venv .venv
* активировать виртуальную среду(Windows): .venv\Scripts\Activate.ps1
* активировать виртуальную среду(Linux): source .venv/bin/activate
* установить зависимости: pip install -r requirements.txt
* используйте .env_sample как образец для создания .env , чтобы настроить переменные окружения
* установить PostgreSQL: sudo apt-get install postgresql postgresql-contrib и sudo systemctl start postgresql
* создать базу данных: sudo -u postgres psql -c "CREATE DATABASE ${POSTGRES_DB};"
* выполнить миграцию: python manage.py makemigrations && python manage.py migrate
* запустить проект: python manage.py runserver
* создать суперпользователя: python manage.py createsuperuser
* создать суперпользователя (кастомная конфигурация):python manage.py create_su
* в консоли запустить celery: celery -A config worker -l INFO
* в консоли запустить celery beat: celery -A config beat -l INFO

## Стек технологий:

* Python 3.11
* Django
* Django Rest Framework
* PostgreSQL
* Redis
* Celery
* Celery Beat
* JWT
* Docker
* Docker Compose
* CORS
* Unittest
* Swagger
* Redoc
* flake8

## Структура проекта:

Проект на Django и Django Rest Framework, включает в себя два приложения "Модули" и "Пользователи".

Структура проекта:

* modules - приложение "Модули"
* users - приложение "Пользователи"
* admin - приложение (дефолтное) "Администратор" (доступно только администратору)

## Модули:

Модель "Модули" содержит следующие поля:

* serial_number - порядковый номер модуля
* name - название модуля
* description - описание модуля
* image - изображение модуля
* url_video - ссылка на видео
* last_update - дата обновления модуля
* owner - владелец модуля
* is_published - опубликован ли модуль
* views_count - количество просмотров
* likes - количество лайков
* liked_users - пользователи, которые лайкнули модуль

## Пользователи:

Модель "Пользователи" содержит следующие поля:

* email - почта пользователя
* first_name - имя пользователя
* last_name - фамилия пользователя
* password - пароль пользователя
* is_active - активирован ли пользователь
* is_staff - сотрудник ли пользователь
* is_superuser - суперпользователь
* last_login - дата последнего входа пользователя
* telegram - ссылка на профиль в Telegram
* confirmation_code - код подтверждения
* role - роли пользователя

## Права доступа:

Права доступа на модули и пользователи могут быть присвоены роли. В роли пользователя может быть "Администратор", "Модератор", "Пользователь". Чтобы пользователь мог заходить на сайт, нужно подтвердить свою почту по ссылке, отправленной на почту после регистрации.

## Тесты:

Тесты проекта запускаются командой python manage.py test

Запустить подсчет покрытия и вывести отчет: coverage run --source='.' manage.py test && coverage report

## Настройки для развертывания и администрирования проекта с помощью Docker:

* для создания образа используйте команду: docker-compose build
* для запуска проекта используйте команду: docker-compose up
* для остановки проекта используйте команду: docker-compose down
* для удаления образа используйте команду: docker-compose rm -f
* для удаления контейнеров используйте команду: docker-compose rm -f -s
* для перезапуска контейнеров используйте команду: docker-compose up -d
* чтобы посмотреть статус проекта: docker-compose ps
* чтобы посмотреть логи проекта: docker-compose logs
* попасть в базу данных PostgreSQL можно следующим образом: docker compose exec db psql -U {POSTGRES_USER=из .env} -d {POSTGRES_DB=из .env}
* создать суперпользователя можно следующим образом: docker compose exec app python manage.py createsuperuser или docker compose exec app python manage.py create_su (будут использованы параметры из секции # Настройки администратора сервиса из .env)
* можно использовать заполнение фикстур с помощью команды: docker compose exec app python manage.py loaddata some_fixtures.json

## Документация:

Документация проекта доступна по адресу:

`http://127.0.0.1:8000/swagger/`
`http://127.0.0.1:8000/redoc/`
