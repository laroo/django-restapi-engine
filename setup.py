import os

from setuptools import setup

# Readme as long description
with open(os.path.join(os.path.dirname(__file__), "README.md")) as readme_file:
    long_description = readme_file.read()

setup(
    name="django-restapi-engine",
    packages=[
        "django_restapi_engine",
    ],
    url="https://github.com/laroo/django-restapi-engine",
    project_urls={
        "Documentation": "https://github.com/laroo/django-restapi-engine",
        "Source": "https://github.com/laroo/django-restapi-engine",
        "Tracker": "https://github.com/laroo/django-restapi-engine/issues",
    },
    license="MIT",
    author="Jan-Age Laroo",
    description="Use any RestAPI as basic Django Database Engine",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires=">=3.7",
    install_requires=["Django~=3.2"],
    zip_safe=False,
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "License :: OSI Approved :: MIT License",
    ],
)
