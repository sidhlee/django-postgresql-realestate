# Using database in Django

In this project, we are using PostgreSQL as a database.

## Setting up database and running db server

1. Download [Postgres.app](https://postgresapp.com/downloads.html) and follow the instruction on "Installing Postgres.app"
2. Double click on `postgres` db to start PostreSQL interactive terminal.
3. Set the password for the user: postgres by:

   ```txt
   postgres=# \password postgres
   ```

4. Create database owned by `postgres` user

   ```txt
   postgres=# CREATE DATABASE btredb OWNER postgres;
   ```

5. Check created db by typing `\l`
6. Exit by `\q`

## Using pgAdmin

1. Install [pgAdmin](https://www.pgadmin.org/)
2. Right click on Servers and select Create > Server
3. Set server name (dbserver), hostname(localhost), Username(postgres), and Password you set for the user, then click on save.
4. Now dbserver is created under Servers which has btredb you created on postgres prompt.
5. Right click on btredb then select Property > Security, then add "postgres" as Grantee and check "All" under Privileges. Save to close window.

## Installing PostgreSQL adapter and update settings.py

Inside the virtual environment, install [pycopg](https://pypi.org/project/psycopg2/):

```bash
pip install psycopg2 psycopg2-binary
```

Now change the default database inside the settings.py

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'btredb',
        'USER': 'postgres',
        'PASSWORD': <User Password>,
        'HOST': 'localhost'
    }
}
```

## Creating database models

When you install a django app, `models.py` file is created. You can create the model class inside this file that maps into the database table.

```python
from django.db import models
from datetime import datetime

class Realtor(models.Model):
  name = models.CharField(max_length=200)
  photo = models.ImageField(upload_to='photos/%Y/%m/%d/')
  description = models.TextField(blank=True)
  phone = models.CharField(max_length=20)
  email = models.CharField(max_length=50)
  is_mvp = models.BooleanField(default=False)
  hired_date = models.DateTimeField(default=datetime.now, blank=True)
  def __str__(self):
    return self.name
```

After writing the model class, run `makemigrations` option to create the actual migration file. If there's dependency error, install necessary packages.

```bash
python manage.py makemigrations
```

## Running migrations

Django propagates changes to the models to the database with "migration",
and there are some built-in admin models that need to be migrated into the database.

Run the following command to migrate these models into PostgreSQL tables:

```bash
python manage.py migrate
```

You can check the tables create in your database via pgAdmin.

## Reference

- [Django Model field reference](https://docs.djangoproject.com/en/3.2/ref/models/fields/)
- [Django Migrations: A Primer](https://realpython.com/django-migrations-a-primer/)
