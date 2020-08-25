# migrating-database

### Description

Flask application to migrate database from mariadb to mongodb

### Tools & Libraries

- Python/Flask
- mariadb
- mongodb (flask_mongoengine)
- asyncio


### How to run project

- edit configuration of mongodb and mariadb

```sh
$ pip install -r requirenments.txt
```

```sh
python app.py
```

```
 curl 127.0.0.1:5000/migrate/employee
 Response 200 OK
```

```
 curl 127.0.0.1:5000/showmongodb/employee/page/offset
 Response 200 OK
```
