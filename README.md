# django-restapi-engine

Use any RestAPI as basic Django Database Engine

## About

A simple Django database engine that interfaces with any RestAPI and perform basic CRUD actions.

![](https://raw.githubusercontent.com/laroo/django-restapi-engine/main/example_projects/jsonplaceholder_project/django-admin-demo.gif)

## Motivation

To interact with rest API's I was creating scripts using `curl` or `Postman` UI. This is quite
cumbersome and often fails as it's missing proper validation and a easy UI.

With Django admin it's possible to create a customizable CRUD interface in a few simple lines of
code, but it only works on database backends. Leveraging Django admin for CRUD operations by
defining a basic database engine that interfaces with any RestAPI.

## Usage

### Installation


Stable version:

    pip install django-restapi-engine


Development version:

    pip install git+https://github.com/laroo/django-restapi-engine.git@main

### Create RestAPI handler

Create a custom RestAPI handler that implements all methods from `BaseRestApiHandler`

    from django_restapi_engine.rest_api_handler import BaseRestApiHandler

    class MyCustomRestApiHandler(BaseRestApiHandler):

        def list(self, *, model, columns, query):
            return [
                return {'id': 1`, 'title': 'some title'},
                return {'id': 2`, 'title': 'another title'}
            ]

        def get(self, *, model, pk, columns):
            return {'id': 1`, 'title': 'some title'}

        def insert(self, *, model, obj, fields, returning_fields):
            return {'id': 3`}

        def update(self, *, model, pk, values):
            return 1

        def delete(self, *, model, pk):
            return


### Django Database Configuration

In Django's `settings.py` add a new database config after the `default` connection
with the following settings:

- `ENGINE`: Tell Django to use `django_restapi_engine`
- `DEFAULT_HANDLER_CLASS`: Point to your custom RestAPI handler class created in previous step

Example:

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'restapi': {
            'ENGINE': 'django_restapi_engine',
            'DEFAULT_HANDLER_CLASS': 'module.location.of.MyCustomRestApiHandler'
        }
    }


### Usage

    # Create
    todo = Todo(
        user_id=123,
        title="My new todo!",
        completed=False
    )
    todo.save(using="restapi")

    # Read
    todo = Todo.objects.using('restapi').get(pk=1)

    # Update
    todo.title = "New title!"
    todo.save(using="restapi")

    # Delete
    todo.delete(using="restapi")

    # List
    Todo.objects.using('restapi').all()


### Django Admin Configuration

Create custom admin class that extends `ModelAdmin` to point to the new database connection:

    class RestApiModelAdmin(admin.ModelAdmin):

        def save_model(self, request, obj, form, change):
            obj.save(using='restapi')

        def delete_model(self, request, obj):
            obj.delete(using='restapi')

        def get_queryset(self, request):
            return super().get_queryset(request).using('restapi')


See [example project](example_projects/jsonplaceholder_project/todos/admin.py)

## Example Project

See [README.md](https://github.com/laroo/django-restapi-engine/blob/main/example_projects/jsonplaceholder_project/README.md) in `example_projects/jsonplaceholder_project`

## Limitations

There is no support for relationships like `ForeignKey` and `ManyToManyField`
