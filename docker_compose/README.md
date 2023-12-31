# Настройка проекта
Перейдите в папку docker_compose/simple_project и выполните docker compose up -d. Будет создан образ приложени, базы, nginx и swagger.

Переменные окружения для подключения к базе данных должны быть описаны в файле .env, расположеном в папке simple_project.
Пример файла:

```
POSTGRES_USER=app
POSTGRES_PASSWORD=123qwe
POSTGRES_HOST=db
POSTGRES_PORT=5432
POSTGRES_DB=movies_database
SECRET_KEY = 'django-insecure-@k04vsjy@qv3m573&94kgq_kjj@lad^^d%hr_o2sk!a6+c3ne9'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,[::1]
```

Теперь, для заполнения БД проверочными данными вы можете запустить docker exec -it service python manage.py loaddata /opt/app/fixtures/fixture.json.

Так же нужно создать пользователя docker exec -it service python manage.py createsuperuser

После этого админка с записями должна стать доступна на локальном хосте по адресу http://localhost/admin/

API V1 будет доступно по адресу http://localhost/api/v1/movies/

# Проектное задание: Docker-compose

Приступим к улучшению сервиса в области DevOps. Настройте запуск всех компонентов системы — Django, Nginx и Postgresql — с использованием docker-compose.

Для упрощения выполнения задания мы подготовили проект, где настроена работа связки Django + uWSGI + Nginx + Docker. Вы можете взять его за основу, но его придётся дополнительно доработать, чтобы подключить Postgres, а также устранить мелкие ошибки в конфигурировании Django: например, `debug = True` или отсутствие настроек чтения переменных окружения.

Сама заготовка уже показывает админку с примером одного метода API. Однако статика не собирается, миграций нет, конфиги Nginx, uWSGI и Docker, возможно, придётся подправить.

Если вы считаете, что всё нужно сделать по-другому, воспользуйтесь пустой заготовкой проекта и напишите его самостоятельно.

**Требования к работе:**

- Напишите dockerfile для Django.
- Для настройки Nginx можно пользоваться наработками из этой темы, но ревьюеры будут запускать ваше решение. Перед сдачей проекта убедитесь, что всё работает правильно.
- Уберите версию Nginx из заголовков. Версии любого ПО лучше скрывать от посторонних глаз, чтобы вашу админку случайно не взломали. Найдите необходимую настройку в официальной документации и проверьте, что она работает корректно. Убедиться в этом можно с помощью «Инструментов разработчика» в браузере.
- Отдавайте статические файлы Django через Nginx, чтобы не нагружать сервис дополнительными запросами. Перепишите `location` таким образом, чтобы запросы на `/admin` шли без поиска статического контента. То есть, минуя директиву `try_files $uri @backend;`.

**Подсказки и советы:**

- Теории на платформе должно быть достаточно для понимания принципов конфигурирования. Если у вас появятся какие-то вопросы по параметрам, ищите ответы [в официальной документации](https://nginx.org/ru/).
- Для выполнения задачи про `/admin` нужно посмотреть порядок поиска `location`.
- Для работы со статикой нужно подумать, как залить данные в файловую систему контейнера с Nginx.
- Для задания дана базовая структура, которой можно пользоваться.
- При настройке docker-compose важно проверять пути до папок. Большинство проблем связанно именно с этим.
