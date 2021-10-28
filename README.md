## Description
At this project just shows a flask project structure which is designed with mvc architecture,
ofcourse because it's an REST Full API, just contains model and view parts.

- PostgreSQL (object-relational database) as a main database
- Flask-RESTful ( support building REST APIs)
- Flask-SQLAlchemy extension which  support for SQLAlchemy (the python SQL toolkit and ORM)
- Flask-Marshmallow  which support for marshmallow(an object serialization/deserialization library(ofcourse use for validation))
- celery as a asynchronous task queue in order to run background tasks (to execute tasks outside of the context of application) and use redis as it's message broker 
- redis-py library in order to use resis (in-memory data structure store) as a cache  to improve performance
- MongoEngine (an Object-Document Mapper) for get reports

## Install Environments
```bash
sudo apt install python3-venv
python3.9 -m venv venv
source venv/bin/activate
pip install wheel
pip install -r requirements.txt
```

## config .env
open .env.example file in application folder and set env then rename file to .env


## Setup Database
when your venv is activate run:
```bash
python manage.py db create_db
python manage.py db seed_db
```

## RUN Project
when your venv is activate run:
```bash
python develop.py
```

## RUN Tests
when your venv is activate run:
```bash
pytest
```

## Example Error Format
```bash
{
    "error": {
        "mobile": "mobile is required"
    },
    "success": false
}
```


## manage.py commands
these comment should be run with active venv:

for Create database structure
```bash
python manage.py create_db
```

for Drop database
```bash
python manage.py drop_db
```

for Seed database with example data
```bash
python manage.py seed_db
```

for detele mongo collection
```bash
python manage.py drop_collection_mongo
```

for detele special item from special tabale
```bash
python3 manage.py del_object <Model Name> <item id>
```

