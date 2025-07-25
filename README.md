

# WhiteRock: v2

Group Repository for COSC 4353 Software Design

---

## 🚀 Run Locally (WSL/Linux/Mac)

These are instructions for running the project on WSL. The process is similar for Linux and macOS.

> ⚠️ **Before starting**, get the database username and password from `Nightterrors` on Discord.

### 🔧 Setup Instructions

```bash```
# Open Powershell and enter WSL
wsl

# Clone the repository
git clone git@github.com:alijavaidistar/WhiteRock.git
cd WhiteRock

# Install required system dependencies
sudo apt update
sudo apt install python3 python3-pip python3-django
sudo apt install python3.10-venv
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

# Install MySQL CLI
sudo apt install mysql-server

# Connect to the database
mysql --host=whiterockdb.mysql.database.azure.com --user=<USER> --password=<PASSWORD> --port=3306 --database=mjapp


# Clone the repository
git clone git@github.com:alijavaidistar/WhiteRock.git
cd WhiteRock

# Build and start containers
docker-compose build
docker-compose up

# Apply migrations
docker-compose exec web python manage.py migrate

# (Optional) Create a superuser
docker-compose exec web python manage.py createsuperuser

