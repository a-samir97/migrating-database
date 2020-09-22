from migrate_tools.mongodb.init_db import db

class Address(db.Document):
    address_id = db.IntField()
    city = db.StringField()
    state = db.StringField()
    country = db.StringField()
    employee_id = db.IntField()
