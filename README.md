<<<<<<< HEAD
# WhiteRock
Group Repo for Software Design Project

# Open Powershell and enter WSL
wsl

# Clone repo and go to django_app 
git clone https://github.com/Nighttterrors/TeamMooseJaw.git
cd TeamMooseJaw

# Install dependencies if you don't already have them
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-django
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
sudo apt install python3.10-venv

#Environment Variables
Before running the application, you need to create a `.env` file in the `django_app` directory with the following Microsoft Oauth credentials:

TENANT_ID=7ce5bdd5-fdda-44b4-a37d-c69818c0d01a
CLIENT_ID=fa2e1d80-7b4a-4d99-8c42-b8075affdd93
CLIENT_SECRET=<GET_FROM_christaO2> #### if you are the TA Please check the assignment Implementation of v0.2 submission2 Github doesn't allow to push secrets


# Start server
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt 
export DB_USER=<USER>
export DB_PASSWORD=<PASSWORD>
python3 manage.py runserver


Run with Docker
These instructions will help you run the application using Docker and Docker compose

Prerequistes 
Make sure you have the following installed:

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/) 
- Git 

# 1. Clone the repository
git clone git@github.com:alijavaidistar/WhiteRock.git
cd WhiteRock

# 2. Build and start the containers
docker-compose build
docker-compose up

# 3. Run database migrations
docker-compose exec web python manage.py migrate

# 4. (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser
=======
# White Rock v2:
Group Repository for COSC 4353 Software Design


## Run Locally
These are instructions for WSL but the process should be similar for Mac/Linux systems.

```
# Open Powershell and enter WSL
wsl

# Clone repo and go to django_app 
git clone https://github.com/alijavaidistar/WhiteRock/
cd WhiteRock
>>>>>>> 38b042086d3ac7693a2ecf208ccabf49514a3576

# Install dependencies if you don't already have them
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-django
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

TENANT_ID=170bbabd-a2f0-4c90-ad4b-0e8f0f0c4259
CLIENT_ID=92088f70-53f7-4321-a0af-85f9463af0c0
CLIENT_SECRET=Get it from mominnaim

export DB_USER=<YOUR_USERNAME>
export DB_PASSWORD=<YOUR_PASSWORD>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
```

# Query Database
These are instructions for WSL to connect to the database and run queries. The process should be similar for Mac/Linux Systems.
```
# Install MySQL cli
sudo apt install mysql-server

# Connect to the database
 mysql --host=moosejawdb.mysql.database.azure.com --user=<USER> --password=<PASSWORD> --port=3306 --database=mjapp
 
# List dbs, tables, and columns
mysql> show databases;
mysql> show tables;
mysql> show columns from users;

# Run query
mysql> select * from users;
 
# Exit
mysql> exit
```
# Run with Docker

Prerequisites
make sure you have the following installed:
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Git
```
# 1. Clone the repository
git clone https://github.com/alijavaidistar/WhiteRock
cd White Rock

# 2. Build and start the containers
docker-compose build
docker-compose up

# 3. Run database migrations
docker-compose exec web python manage.py migrate

# (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser
```
