#  Cities Project
A web application for exploring cities, providing detailed information about weather, history, and current conditions. Built with Django and PostgreSQL

## Requirements
- Python 3.12
- Poetry
- PostgreSQL

---

## Installation

### 1. Clone the repository
Clone the project to your local machine:
```bash
git clone git@github.com:OndraJ/cities.git
cd cities
```

### 2. Activate the virtual environment

```bash 
poetry shell
```

### 3. Install dependencies

```bash
poetry install
```

###  4. Create a PostgreSQL database

Create a user and a database in PostgreSQL:
```bash
CREATE USER cities_user WITH PASSWORD 'securepassword';
CREATE DATABASE cities_db OWNER cities_user;
GRANT ALL PRIVILEGES ON DATABASE cities_db TO cities_user;
```
Reset and reassign the public schema (if necessary)
```bash
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public AUTHORIZATION cities_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO cities_user;
```
### 5. Configure the environment variables

Create a .env file in the root project directory and add the following environment variables:
```bash
DB_NAME=cities_db
DB_USER=cities_user
DB_PASSWORD=securepassword
DB_HOST=localhost
DB_PORT=5432
```
### 6. Run the migrations

```bash
poetry run python manage.py migrate
```

### 7. Run the server

```bash
poetry run python manage.py runserver
```

---

## Troubelshooting

### Peer authentication error
If you encounter the error
```bash
Peer authentication failed for user "cities_user"
```
1. open the pg_hba.conf file
```bash
sudo nano /etc/postgresql/[version]/main/pg_hba.conf
```
2. Replace `peer` with `md5`
```bash
local   all             all                                     md5
```
3. Save the file and restart PostgreSQL:
```bash
sudo service postgresql restart
```

### Permission Denied for Schema Public

If you encounter the error
```bash
permission denied for schema public
```
Ensure the user has the correct permissions:

1. Log in to PostgreSQL as the postgres superuser:
```bash
sudo -u postgres psql
```
2. Reset the public schema and grant permissions:
```bash
DROP SCHEMA IF EXISTS public CASCADE;
CREATE SCHEMA public AUTHORIZATION cities_user;
GRANT ALL PRIVILEGES ON SCHEMA public TO cities_user;
```
3. Exit the PostgreSQL shell:
```bash
\q
```
4. Restart the PostgreSQL service:
```bash
sudo service postgresql restart
```
5. Run the migrations again:
```bash
poetry run python manage.py migrate
```
