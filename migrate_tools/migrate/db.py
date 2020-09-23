import mariadb
import asyncio
import os

from migrate_tools.models.address import Address
from migrate_tools.models.employee import Employee

def executequery(sql="",params=[]):

    # connection for mariadb
    if os.environ.get("FLASK_ENV") == 'docker_development':
        from migrate_tools.config.base_config import DockerDevelopmentConfig
        MARIA_CONFIG = DockerDevelopmentConfig.MARIA_CONFIG

    elif os.environ.get("FLASK_ENV") == 'local_development':
        from migrate_tools.config.base_config import LocalDevelopmentConfig
        MARIA_CONFIG = LocalDevelopmentConfig.MARIA_CONFIG

    connection = mariadb.connect(**MARIA_CONFIG)

    # create cursor
    cur = connection.cursor()

    # "ahmed is %s and  %s" % ("Good", "Great")
    # "select * from employee where name =ahmed and age=30"
    # "select * from employee where name =%s and age=%s"
    # "select * from employee where name =%s and age=%s" % tuple(["ahmed",30])

    sql = sql % tuple(params)

    # excute query
    cur.execute(sql)

    # serialize results into JSON
    all_data = cur.fetchall()

    # close connection 
    connection.close()
    
    return all_data


async def migrate_data():
    
    # serialize results into JSON
    all_data = executequery("SELECT * from employee")

    # debugging before starting migration
    print("Migration Start")

    # migrate all database from mariadb to mongodb
    for result in all_data:
        
        # get address for every employee 
        all_address_data = executequery("Select * from address where employee_id=%s", [str(result[0])])        

        # list of employee address 
        employees_address_list = []

        for address in all_address_data:        
            new_address = Address(
                address_id=address[0] if address[0] else None,
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
            address=employees_address_list)

        new_employee.save()


        employees_address_list = []

    # debugging after finishing migration
    print("Migration Finished !!")