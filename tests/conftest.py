def pytest_configure():
    from django.conf import settings

    MIDDLEWARE = ("django.middleware.common.CommonMiddleware",)

    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES={
            "default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory:"},
            "restapi": {
                "ENGINE": "django_restapi_engine",
                "DEFAULT_HANDLER_CLASS": "tests.conftest.FakeRestApiHandler",
            },
        },
        SITE_ID=1,
        SECRET_KEY="dummy test secret",
        USE_I18N=True,
        STATIC_URL="/static/",
        ROOT_URLCONF="tests.urls",
        TEMPLATES=[
            {
                "BACKEND": "django.template.backends.django.DjangoTemplates",
                "APP_DIRS": True,
            },
        ],
        MIDDLEWARE=MIDDLEWARE,
        MIDDLEWARE_CLASSES=MIDDLEWARE,
        INSTALLED_APPS=(
            "django.contrib.auth",
            "django.contrib.contenttypes",
            "django.contrib.sessions",
            "django.contrib.sites",
            "django.contrib.staticfiles",
            "tests",
        ),
        PASSWORD_HASHERS=("django.contrib.auth.hashers.MD5PasswordHasher",),
    )

    try:
        import django

        django.setup()
    except AttributeError:
        pass
