from flask import Blueprint, request, Response, jsonify

# create blueprint for database routes 
database_routes = Blueprint('database_routes', __name__)

@database_routes.route('config', methods=['POST'])
def database_configuration():
    '''
        Database configuration in runtime.

        List of selected database: 
            1- Postgres
            2- Mariadb
            3- MySQL
    '''
    data = request.get_json()

    if data.get('type') == 'postgres':
        
        # use psycopg2 library to connect to postgres database
        POSTGRES_CONFIG = {
            'host': data['host'],
            'database': data['database'],
            'user': data['user'],
            'password': data['password']
        }

    elif data.get('type') == 'mariadb':

        # use mariadb library to connect to maria database
        MARIA_CONFIG = {
            'host': data['host'],
            'port': data['port'],
            'user': data['user'],
            'password': data['password'],
            'database': data['database']
        }    

    elif data.get('type') == 'mysql':
        # use pymysql library to connect to mysql database
        # or use mysql connector library to connect mysql database

        MYSQL_CONFIG = {
            'host': data['host'],
            'user': data['user'],
            'password': data['password'],
            'database': data['database']
        }
        
    else:
        return Response(status=404)