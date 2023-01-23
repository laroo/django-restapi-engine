
# Example project: typicode/json-server


This example project uses the full fake REST API from [typicode/json-server](https://github.com/typicode/json-server)

Please note that this API is readonly and changes (insert, update & delete) won't be applied!

## Running example project


1. Create and activate Virtual Environment

        python3 -m venv .venv
        source .venv/bin/activate

2.  Install requirements:

        pip install -r requirements.txt

3.  Create local SQLite database:

        python manage.py migrate

4.  Load sample data:

        python manage.py loaddata mysite/fixtures/initial_data

5.  Run Django server:

        python manage.py runserver

6.  Install JSON server:

        npm install -g json-server

6.  Run JSON server:

        json-server --watch db.json


6. Take a look at:
    - Movies view: <http://127.0.0.1:8000/books/>
    - Django Admin: <http://localhost:8000/admin/> (log in with username `admin` and password `admin`)
