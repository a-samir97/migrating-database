import mariadb, mysql.connector, psycopg2

def connect_database(type, config):

    if type == 'postgres':
        connection = psycopg2.connect(**config)
        return connection

    elif type == 'mysql':
        connection = mysql.connector.connect(**config)
        return connection
    
    elif type == 'mariadb':
        connection = mariadb.connect(**config)
        return connection 

    return None