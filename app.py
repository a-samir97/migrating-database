import asyncio
from flask import Flask, Response, jsonify
import mariadb

from flask_mongoengine import MongoEngine



# create flask app 
app = Flask(__name__)
app.config['DEBUG'] = True

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

class Address(db.Document):
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    employee_id = db.IntField()

class Employee(db.Document):
    employee_id = db.IntField()
    name = db.StringField()
    age = db.IntField()
    address = db.ListField(db.ReferenceField(Address))

# steps 
# convert from mariadb to mongodb with all relations 
# employee with age, name, id ==> this is the first table here 
# another table with Address with country, state, city , employee_id (foreign key)
# document after migrating database
''' 
{
    "employee_id": "1",
    "name": "Ahmed Samir",
    "age": 22,
    "Address": {
        "country": "Egypt",
        "state": "Cairo",
        "city": "New Cairo"
    }
 }
 ''' 

async def migrate_data():
    
    # connection for mariadb 
    connection = mariadb.connect(**config)
    
    # create cursor
    cur = connection.cursor()
    cur2 = connection.cursor()

    # excute query
    cur.execute("Select * from employee")
    

    # serialize results into JSON
    all_data = cur.fetchall()

    # migrate all database from mariadb to mongodb
    for result in all_data:
        
        # get address for every employee 
        cur2.execute("Select * from address where employee_id={}".format(result[0]))        
        
        # fetch all data of the selected employee 
        all_address_data = cur2.fetchall()
        
        # list of employee address 
        employees_address_list = []

        for address in all_address_data:        
            new_address = Address(
                state=address[1] if address[1] else None, 
                country=address[2] if address[2] else None, 
                city=address[3] if address[3] else None, 
                employee_id=address[4] if address[4] else None
            )
            new_address.save()
            employees_address_list.append(new_address)
        
        new_employee = Employee(
            employee_id=result[0], 
            name=result[1], 
            age=result[2], 
            address=[new_address])

        new_employee.save()


        employees_address_list = []

# async call 
# return 200 status code 
@app.route('/migrate/employee', methods=['GET'])
def index():
    # call the async task 
    asyncio.run(migrate_data())
    # return the results!
    return Response({"Processing... Please wait"},200)
    
@app.route('/showmongodb/employee/<page>/<offset>', methods=['GET'])
def show_mongodb_docs(page, offset):

    paginated_employees_data = Employee.objects.paginate(page=int(page), per_page=int(offset)).items

    json_data = []

    json_address = []

    # serializing data to json 
    for item in paginated_employees_data:
        for address in item.address:
            json_address.append({
                'city': address.city,
                'country': address.country,
                'state': address.state,
                'employee_id': address.employee_id
            })

        json_data.append({
            'name': item.name,
            'age': item.age,
            'address': json_address,
        })    

        json_address = []
    
    return jsonify(json_data)

# run app 
app.run()