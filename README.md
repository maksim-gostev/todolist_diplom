# Todolist
## _Приложенеие "Календарь" для работы с задачами_

***

# Стек технологий

- [Python 3.10](https://www.python.org/)
- [Django 4.2.2](https://www.djangoproject.com/)
- [Django REST Framework 3.14.0](https://www.django-rest-framework.org/)
- [Postgres 15.2](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Pydantic](https://docs.pydantic.dev/dev-v1/)
- [Poetry](https://python-poetry.org/)
- [VK OAuth 2.0](https://dev.vk.com/ru/api/access-token/getting-started)
- [GitHub Actions](https://docs.github.com/en/actions)
- [pytest-django](https://pytest-django.readthedocs.io/en/latest/index.html)
- GitHub Actions

### Функционал
>* Регистрация и авторезация с помощью вашего акунты VK
>* Создание, обновление, удаление досок объявлений и возможность делится ими
>* Создание, обновление, удаление категорий
>* Создание, обновление, удаление целей
>* Просмотр и создание целей с помощью Telegram-бота
>* Назначени приорететов и установка дедлайнов
>* Завершённые задачи отправляются в архив


### Установка
* Скачайте исходники c GitHub
* Заполните файл `.env` в соответствии с шаблоном `.env.example`
* Запустите `docker-compose up -d`
* Создайте приложение в ВК
* Полученный при регистрации `ID` присвойте константе SOCIAL_AUTH_VK_OAUTH2_KEY, а защищённый ключ константе SOCIAL_AUTH_VK_OAUTH2_SECRET в файле `.env`
* Если приложение развернуто на локальной машине наберите в адресной строке браузера `http://localhost`, если на сервере адрес данного сервера в сети интернет

### Ссылки на проект

* [Сайт](http://158.160.113.253)
* [Telegram-бота](https://t.me/Todolist_15_bot)

### Где скачать:
[GitHub](https://github.com/maksim-gostev/todolist_diplom.git)
