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
        cur.execute("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS \
                    WHERE TABLE_NAME = '%s';" % table_name)

    all_columns = cur.fetchall()

    # for react 
    json_column = [{'title': x, 'dataIndex': x, 'key': x} for x in all_columns ]

    cur.execute('SELECT * FROM %s;' % table_name)
    all_data = cur.fetchall()

    json_data = []
    for i in range(0, len(all_data)):
        data_dict = {}
        data_dict['key'] = i
        for j in range(0,len(all_columns)):
            col_name = "".join(all_columns[j])
            data_dict[col_name] = all_data[i][j]
        json_data.append(data_dict)

    return jsonify(json_column, json_data)


@database_routes.route('<table_name>/insert', methods=['POST'])
@cross_origin()
def insert_row(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)

    data = request.get_json()

    cur = connection_dict['connection'].cursor()

    columns = ",".join(data.keys())
    values = ",".join(data.values())

    try:
        # execute query
        cur.execute("INSERT INTO %s (%s) VALUES %s;" % (table_name, columns, tuple(data.values())))
    
        # to save changes
        connection_dict.get('connection').commit()

        # return response 201 
        return Response(status=201) # created !!
    except:
        return Response(status=400)

@database_routes.route('<table_name>/delete/<id>', methods=['DELETE'])
@cross_origin()
def delete_row(table_name, id):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)

    cur = connection_dict['connection'].cursor()

    # get primary column
    cur.execute("SELECT c.column_name\
                FROM information_schema.key_column_usage AS c\
                LEFT JOIN information_schema.table_constraints AS t\
                ON t.constraint_name = c.constraint_name\
                WHERE t.table_name = '%s' AND t.constraint_type = 'PRIMARY KEY';" % (table_name,))
    
    # fetch table 
    get_primary_column = cur.fetchone()

    if get_primary_column:
        
        # delete selected row
        cur.execute("DELETE FROM %s WHERE %s=%s" % (table_name, get_primary_column[0], id))

        # to save changes
        connection_dict.get('connection').commit()
    
        # return response
        return Response(status=204)
    
    # row not found
    return Response(status=404)

@database_routes.route('<table_name>/update', methods=['PUT'])
@cross_origin()
def update_row(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)

    # get requested data
    data = request.get_json()

    # cursor for execution query
    cur = connection_dict['connection'].cursor()

    # get primary column
    cur.execute("SELECT c.column_name\
                FROM information_schema.key_column_usage AS c\
                LEFT JOIN information_schema.table_constraints AS t\
                ON t.constraint_name = c.constraint_name\
                WHERE t.table_name = '%s' AND t.constraint_type = 'PRIMARY KEY';" % (table_name,))
    
    # fetch table
    get_primary_column = cur.fetchone()
    
    if get_primary_column:
        
        column_id = data['primaryKey']
        del data['primaryKey']

        # make string to pass it to the query
        query_string = "" 
        for key,value in data.items():
            query_string += "%s='%s'," % (key, value)

        try:
            
            # table name, (column=newfield), (id_column), id field 
            cur.execute("UPDATE %s SET %s WHERE %s=%s" % (table_name, query_string[:-1], get_primary_column, column_id))
        
            # to save changes
            connection_dict.get('connection').commit()
        
            # return response OKK
            return Response(status=200)    

        except:
            return Response(status=400)
    else:
        return Response(status=400)


@database_routes.route('<table_name>/search', methods=['POST'])
@cross_origin()
def search(table_name):

    if connection_dict.get('connection') is None or connection_dict.get('type') is None:
        return Response("There is something not valid, please make your configuration",status=400)

    data = request.get_json()

    # cursor for execution query
    cur = connection_dict['connection'].cursor()

    # to make query string to pass it 
    query_string = ""
    for key, value in data.items():
        query_string += "%s='%s'," % (key, value)

    try:
        # execute query
        cur.execute('SELECT * FROM %s WHERE %s;' % (table_name, query_string[:-1]))

        # fetching 
        all_data = cur.fetchall()

        return jsonify(all_data)

    except Exception as e:
        print(e)
        return Response(status=404)