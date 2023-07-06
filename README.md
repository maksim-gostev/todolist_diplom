# Todolist
## _Приложенеие "Календарь" для работы с задачами_

***

# Стек технологий

- [Python 3.10](https://www.python.org/)
- [Django 4.2.2](https://www.djangoproject.com/)
- [Django REST Framework 3.14.0](https://www.django-rest-framework.org/)
- [Postgres 15.2](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)

### Функционал
>* Регистрация и авторезация с помощью вашего акунты VK
>* Формирование каталога задач
>* Назначени приорететов и установка дедлайнов
>* Завершённые задачи отправляются в архив


### Установка
* Скачайте исходники c GitHub
* Заполните файл `.env` в соответствии с шаблоном `.env.example`
* Запустите `docker-compose up -d`
* Создайте приложение в ВК
* Полученный при регистрации `ID` присвойте константе SOCIAL_AUTH_VK_OAUTH2_KEY, а защищённый ключ константе SOCIAL_AUTH_VK_OAUTH2_SECRET в файле `.env`
* Если приложение развернуто на локальной машине наберите в адресной строке браузера `http://localhost`, если на сервере адрес данного сервера в сети интернет

### Где скачать:
[GitHub](https://github.com/maksim-gostev/todolist_diplom.git)
