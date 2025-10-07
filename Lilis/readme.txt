# Proyecto - U2 Avance: Seeds + Admin Básico

## Motor de BD
El motor de base de datos utilizado es MySQL corriendo desde WampServer.

## Cómo correr
1. pip install django pymysql python-dotenv cryptography django-crispy-forms crispy-bootstrap5
2. Crear base de datos 'lilis' en MySQL y configurar el archivo .env
3. python manage.py migrate
4. python manage.py createsuperuser
5. python manage.py runserver

## Cómo cargar semillas
python manage.py loaddata fixtures/00_categories.json
python manage.py loaddata fixtures/02_products.json

## Admin de prueba
Usuario: vic    
Clave: vic

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

