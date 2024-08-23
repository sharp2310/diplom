
Приложение для обучения посредством модулей, которые принадлежат образовательному порталу. Регистрация пользователя в системе проходит после подтверждения им ссылки, ссылка на подтверждение приходит на электронный адрес пользователя. Любой пользователь, после регистрации в системе может создавать свои образовательные модули, уроки к модулям, загружать их в систему и редактировать их. Так же, любой пользователь может подписываться на образовательные модули и просматривать их. Вывод списка модулей производится по 15 штук на странице

Запуск проекта с использованием Docker

Клонировать репозиторий https://github.com/sharp2310/diplom
Создайте файл с переменными окружения по примеру с .env_sample
Запустите с помощью команды docker-compose build --up
Создание суперпользователя docker-compose exec app python manage.py csu
Команда для остановки контейнера docker-compose down
Стек технологий:

Python 3.11
Django
Django Rest Framework
PostgreSQL
Redis
Docker
Docker Compose
CORS
Unittest
Swagger
Redoc
Структура проекта: Проект на Django и Django Rest Framework, включает в себя два приложения "Модули" и "Пользователи".

modules - приложение "Модули"
users - приложение "Пользователи"
Модель "Модули" содержит следующие поля:

serial_number - порядковый номер модуля
title - название модуля
description - описание модуля
preview - изображение модуля
last_update - дата последнего обновления модуля
owner - владелец модуля
is_published - опубликован ли модуль
Модель "Уроки" содержит следующие поля:

module - модуль
title - название урока
description - описание урока
preview - изображение урока
video_link - ссылка на видео с валидацией ссылки с youtube
owner - владелец модуля
views_count - количество просмотров
Модель "Подписки" содержит следующие поля:

user - пользователь
module - модуль
Модель "Пользователи" содержит следующие поля:

email - почта пользователя
first_name - имя пользователя
last_name - фамилия пользователя
password - пароль пользователя
is_active - активирован ли пользователь
is_staff - сотрудник ли пользователь
is_superuser - суперпользователь
telegram - ссылка на профиль в Telegram
token - токен
Доступ к приложению

Приложение будет доступно по адресу: http://127.0.0.1:8000/
Админ панель Django: http://127.0.0.1:8000/admin/
Тесты: Тесты проекта запускаются командой python manage.py test Запустить подсчет покрытия и вывести отчет: coverage run --source='.' manage.py test && coverage report

Документация API доступна по адресу: http://127.0.0.1:8000/redoc/ http://127.0.0.1:8000/swagger/
