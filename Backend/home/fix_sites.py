import django, os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'home.settings')
django.setup()
from django.db import connection

with connection.cursor() as cursor:
    cursor.execute("INSERT INTO django_migrations (app, name, applied) VALUES ('sites', '0001_initial', CURRENT_TIMESTAMP);")
    cursor.execute("CREATE TABLE IF NOT EXISTS django_site (id integer NOT NULL PRIMARY KEY AUTOINCREMENT, domain varchar(100) NOT NULL, name varchar(50) NOT NULL);")
    cursor.execute("INSERT OR IGNORE INTO django_site (id, domain, name) VALUES (1, 'localhost:8000', 'localhost');")

print("Sites table and migration record fixed successfully!")