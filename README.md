# WhiteRock
Group Repo for Software Design Project

# Open Powershell and enter WSL
wsl

# Clone repo and go to django_app 
git clone git@github.com:alijavaidistar/WhiteRock.git
cd WhiteRock

# Install dependencies if you don't already have them
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-django
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
sudo apt install python3.10-venv

#Environment Variables
Before running the application, you need to create a `.env` file in the `django_app` directory with the following Microsoft Oauth credentials:

TENANT_ID=170bbabd-a2f0-4c90-ad4b-0e8f0f0c4259
CLIENT_ID=92088f70-53f7-4321-a0af-85f9463af0c0
CLIENT_SECRET=<GET_FROM_Mominnaim> Get it from Naim, Github doesn't allow secrets to be pushed.


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

