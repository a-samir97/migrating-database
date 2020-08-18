from flask import Flask, Response
import mariadb

from flask_mongoengine import MongoEngine

from celery import Celery

# create flask app 
app = Flask(__name__)
app.config['DEBUG'] = True

# Celery Configuration
def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery

# celery
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379',
    CELERY_RESULT_BACKEND='redis://localhost:6379'
)
celery = make_celery(app)

# Mariadb Configuration 
config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'ahmedsamir',
    'password': 'password1',
    'database': 'employees'
}

# Mongodb Configuration
app.config['MONGODB_SETTINGS'] = {
    'db': 'employee',
    'host': 'localhost',
    'port': 27017
}

db = MongoEngine()
db.init_app(app)

class Employee(db.Document):
    employee_id = db.IntField()
    name = db.StringField()
    age = db.IntField()

@celery.task
def migrate_data():
    # connection for mariadb 
    connection = mariadb.connect(**config)
    
    # create cursor
    cur = connection.cursor()

    # excute query
    cur.execute("Select * from employee")
    
    # serialize results into JSON
    rv = cur.fetchall()
    
    for result in rv:
        new_employee = Employee(employee_id=result[0], name=result[1], age=result[2])
        new_employee.save()

# async call 
# return 200 status code 
@app.route('/migrate/employee', methods=['GET'])
def index():
    # call the async task 
    migrate_data.delay()
    # return the results!
    return Response({},200)
    
# run app 
app.run()