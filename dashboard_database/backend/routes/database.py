from flask import Blueprint, request, Response, jsonify
from dashboard_database.backend.database.connection import connect_database
from flask_cors import cross_origin

# create blueprint for database routes 
database_routes = Blueprint('database_routes', __name__)

# inital CONNECTION Dict to hold the connection
connection_dict = {}

@database_routes.route('config', methods=['POST'])
@cross_origin()
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
        connection_dict['connection'] = connect_database('postgres', POSTGRES_CONFIG)
        connection_dict['type'] = 'postgres'

        return Response("Postgres is connected successfully!", status=200)

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
        connection_dict['connection'] = connect_database('mariadb', MARIA_CONFIG)
        connection_dict['type'] = 'mariadb'

        return Response("Mariadb is connected successfully!",status=200)

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
        connection_dict['connection'] = connect_database('mysql', MYSQL_CONFIG)
        connection_dict['type'] = 'mysql'

        return Response("MySQL is connected successfully!", status=200)

    else:
        return Response(status=404)

@database_routes.route('all-tables', methods=['GET'])
@cross_origin()
def get_all_tables():

    print(connection_dict.get('connection'), connection_dict.get('type'))

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)
    
    
    cur = connection_dict['connection'].cursor()

    if connection_dict['type'] == 'postgres':

        cur.execute("SELECT tablename\
            FROM pg_catalog.pg_tables\
            WHERE schemaname != 'pg_catalog' AND  schemaname != 'information_schema';")

    else:

        cur.execute('SHOW TABLES;')

    all_tables = cur.fetchall()
    
    cur.close()

    # convert data to json 
    
    return jsonify(all_tables)

@database_routes.route('table-details/<table_name>', methods=['GET'])
@cross_origin()
def get_table_details(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)

    cur = connection_dict['connection'].cursor()

    if connection_dict['type'] == 'postgres':
        
        cur.execute("select column_name from information_schema.columns where table_schema='public' and \
            table_name='%s';" % table_name)

    else:
        cur.execute('SHOW COLUMNS FROM %s;' % table_name)

    all_columns = cur.fetchall()
    # for react 
    all_columns = [{'title': x} for x in all_columns ]
    return jsonify(all_columns)


@database_routes.route('<table_name>/insert', methods=['POST'])
def insert_row(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)


@database_routes.route('<table_name>/delete', methods=['DELETE'])
def delete_row(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)


@database_routes.route('<table_name>/update', methods=['PUT'])
def update_row(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)


@database_routes.route('<table_name>/search', methods=['GET'])
def search(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)