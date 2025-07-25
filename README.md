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

