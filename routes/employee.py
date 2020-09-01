from flask import Blueprint, Response, jsonify, request
from models.employee import Employee
from models.address import Address
from migrate.db import migrate_data

import asyncio

# Blueprint routes
employees_routes = Blueprint('employees_routes',__name__)


@employees_routes.route('check', methods=['GET'])
def check():
    return Response({"Success OK"},200)

@employees_routes.route('migrate/employee', methods=['GET'])
def index():
    # call the async task
    asyncio.run(migrate_data())
    # return the results!
    return Response({"Processing... Please wait"},200)
    
@employees_routes.route('showmongodb/employee/', methods=['GET'])
def show_mongodb_docs():
    # ToDO: set adefault value for page & offset if they are None

    page = request.args.get('page', default=1)
    offset = request.args.get('offset', default=10)
    paginated_employees_data = Employee.objects.paginate(page=int(page), per_page=int(offset)).items

    json_data = []

    json_address = []

    # serializing data to json 
    for item in paginated_employees_data:
        for address in item.address:
            json_address.append({
                'id':address.address_id,
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