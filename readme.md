# Uchet.kz ToDo test task

Тестовое задание - "Список задач" ToDo

Были выполнены все пункты

## Инструкция для запуска с использованием Docker'а.

1. Установить docker
2. Создать файл .env, можно использовать атрибуты из example.env(Нужно подставить только настройки почты)
3. С помощью команды запустить docker-compose
   ```bash
   docker-compose up --build -d

## Инструкция для запуска без использования Docker.

1. Настройка виртуального окружения

   1.1 Создать и активировать виртуальное окружение

    ```bash
   # Windows:
    python -m venv venv
   .\venv\Scripts\activate
   
   # Linux:
   virtualenv -p python3.8 .venv
   source .venv/bin/activate
    ```
   1.2 Установка необходимых библиотек

    ```bash
    pip install -r requirements.txt
    ```

2. Настройка базы данных

   2.1. Установить PostgreSQL

   2.2. Открыть sql shell

   2.3. Выполнить следующие команды:
    ```postgresplsql
    CREATE DATABASE test_task_uchet_db with encoding='UTF-8' LC_CTYPE='en_US.UTF-8' LC_COLLATE='en_US.UTF-8' TEMPLATE=template0;
    CREATE ROLE test_user WITH PASSWORD 'testpassword';
    GRANT ALL PRIVILEGES ON DATABASE test_task_uchet_db to test_user;
    ALTER ROLE test_user LOGIN CREATEDB;
    ```

3. Установить и запустить Redis сервер

   ```bash
    # Windows 
    Установить "Redis 5.0.10 for Windows" используя msi
   
   # Linux
   sudo apt install redis-server
    ```
4. Запуск celery

   4.1 В командой строке выполнить следующую команду
   ```bash
   # Windows
    celery -A test_uchet_kz worker --loglevel=info -P gevent
   
   # Linux
    celery -A test_uchet_kz worker --loglevel=info
    ```

5. Сделать миграции и создать супер пользователя

    ```bash
    ./manage.py makemigrations
    ./manage.py migrate
    ```

    ```bash
    ./manage.py createsuperuser
   
   email: admin@gmail.com
   password: admin
    ```

6. Запустить сервер и проверить его работу открыв `localhost:8000` в браузере

    ```bash
    ./manage.py runserver
    ```

7. В setting.py установить настройки почты с которой будут отправляться письма
   
   Пример для почтового сервиса mail.ru
    ```
   EMAIL_HOST = 'smtp.mail.ru'
   EMAIL_HOST_USER = 'email-here@mail.ru'
   DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
   EMAIL_HOST_PASSWORD = 'password-here'
   EMAIL_PORT = 465
   EMAIL_USE_SSL = True
    ```

8. Для удобства все запросы собраны в файле Insomnia.json

   8.1 Нужно установить программу Insomnia

   8.2 Импортировать из файла Insomnia.json

9. Для удобства все запросы собраны в коллекцию Postman

    9.1 Нужно установить программу Postman

    9.2 Импортировать из файла uchet_kz_test_task.postman_collection.json