# White Rock v2:
Group Repository for COSC 4353 Software Design


## Run Locally
These are instructions for WSL but the process should be similar for Mac/Linux systems.

print(
# Open Powershell and enter WSL
wsl

# Clone repo and go to django_app 
git clone https://github.com/alijavaidistar/WhiteRock/
cd WhiteRock

# Install dependencies if you don't already have them
sudo apt install python3
sudo apt install python3-pip
sudo apt install python3-django
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential

TENANT_ID=7ce5bdd5-fdda-44b4-a37d-c69818c0d01a
CLIENT_ID=fa2e1d80-7b4a-4d99-8c42-b8075affdd93
CLIENT_SECRET=<GET_FROM_christaO2>

export DB_USER=<YOUR_USERNAME>
export DB_PASSWORD=<YOUR_PASSWORD>

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py runserver
)
# Install MySQL CLI
sudo apt install mysql-server

# Connect to the database
mysql --host=whiterockdb.mysql.database.azure.com --user=<USER> --password=<PASSWORD> --port=3306 --database=mjapp


# Clone the repository
git clone git@github.com:alijavaidistar/WhiteRock.git
cd WhiteRock

Prerequisites
make sure you have the following installed:
- [Docker](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- Git

print(

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
)
