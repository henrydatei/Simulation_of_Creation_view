# Simulation of Creation View
Django project to view the data from https://github.com/SchumPau/Simulation_of_Creation

### Setup
1. Clone the repository
2. Create a `.env` file in the root directory with the following content
```txt
# .env sample

DB_ENGINE=mysql
DB_NAME="db_name"
DB_USERNAME="username"
DB_PASS="password"
DB_HOST=localhost
DB_PORT=3306
```
3. Install the requirements with `pip install -r requirements.txt`
4. Run the migrations with `python manage.py migrate`
5. Run the server with `python manage.py runserver`
6. Open the browser and go to `http://localhost:8000/`
