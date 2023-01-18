
# Example project: JSONPlaceholder

This example project uses the `Todo` rest API from [JSONPlaceholder](https://jsonplaceholder.typicode.com/)

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

5.  Run testing server:

        python manage.py runserver

6. Take a look at:
    - Todo view: <http://127.0.0.1:8000/todos/>
    - Django Admin: <http://localhost:8000/admin/> (log in with username `admin` and password `admin`)
    - Run manage.py command: `python manage.py fetch_todo`
