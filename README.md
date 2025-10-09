# Proyecto - U2 Avance: Seeds + Admin Básico

## Motor de BD
El motor de base de datos utilizado es MySQL corriendo desde WampServer.

## Cómo correr el mejor server de la vida
1. pip install django pymysql python-dotenv cryptography django-crispy-forms crispy-bootstrap5
2. Crear base de datos 'lilis' en MariaDB y configurar el archivo .env
3. python manage.py migrate
4. python manage.py loaddata fixtures/#00,02,03,04
5. python manage.py seed_roles
4. python manage.py createsuperuser
5. python manage.py runserver

## Cómo cargar semillas
python manage.py loaddata fixtures/00_categories.json
python manage.py loaddata fixtures/02_products.json



## Rama para el avance
u2-c2-admin-basico
https://github.com/imVic-Byte/ProjectLilis/tree/u2-c2-admin-basico








DJANGO_SECRET_KEY = supersecret
DJANGO_DEBUG = True
DB_NAME = Lilis
DB_USER = LilisAdmin
DB_PASSWORD = Admin123
DB_HOST = localhost
DB_PORT = 3307






























DJANGO_SECRET_KEY = supersecret
DJANGO_DEBUG = True
DB_NAME = Lilis
DB_USER = LilisAdmin
DB_PASSWORD = Admin123
DB_HOST = localhost
DB_PORT = 3307
