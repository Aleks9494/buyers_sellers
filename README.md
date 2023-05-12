Для запуска:
 - создать БД PosgreSQL "test_shop" с пользователем postgres и паролем 12345
 - создать и запустить миграции БД: python3 manage.py makemigrations, python3 manage.py migrate
 - создать суперпользователя: python3 manage.py createsuperuser
 - запустить: python3 manage.py runserver
 - зайти в админ-панель, создать юзеров, разделить их на покупателей и продавцов, создать лоты и сделки
 - запустить скрипт: python3 manage.py script