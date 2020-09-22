from flask import Blueprint, request, Response, jsonify
from backend.database.connection import connect_database

# create blueprint for database routes 
database_routes = Blueprint('database_routes', __name__)

# inital CONNECTION variable None
connection = None
TYPE = None

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

        # make connection, this function will return the connection
        connection = connect_database('postgres', POSTGRES_CONFIG)
        TYPE = 'postgres'

        return Response(status=200)

    elif data.get('type') == 'mariadb':

        # use mariadb library to connect to maria database
        MARIA_CONFIG = {
            'host': data['host'],
            'port': data.get('port', 3306),
            'user': data['user'],
            'password': data['password'],
            'database': data['database']
        }    

        # make connection, this function will return the connection
        connection = connect_database('mariadb', MARIA_CONFIG)
        TYPE = 'mariadb'

        return Response(status=200)

    elif data.get('type') == 'mysql':
        # use pymysql library to connect to mysql database
        # or use mysql connector library to connect mysql database

        MYSQL_CONFIG = {
            'host': data['host'],
            'user': data['user'],
            'password': data['password'],
            'database': data['database']
        }
        
        # make connection, this function will return the connection
        connection = connect_database('mysql', MYSQL_CONFIG)
        TYPE = 'mysql'

        return Response(status=200)

    else:
        return Response(status=404)


def get_all_tables():

    if connection is None or TYPE is None:
        return Response(status=400)
    
    
    cur = connection.cursor()

    if TYPE == 'postgres':

        cur.execute("SELECT tablename\
            FROM pg_catalog.pg_tables\
            WHERE schemaname != 'pg_catalog' AND  schemaname != 'information_schema';")

    else:

        cur.execute('SHOW TABLES;')

    all_tables = cur.fetchall()

    cur.close()

    # convert data to json 
    
    return Response(jsonify(all_tables), status=200)