from mongodb.init_db import db
from models.address import Address

class Employee(db.Document):
    employee_id = db.IntField()
    name = db.StringField()
    age = db.IntField()
    address = db.ListField(db.ReferenceField(Address))