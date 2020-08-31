import mariadb

def executequery(sql="",params=[]):
    # connection for mariadb
    connection = mariadb.connect(**config)

    # create cursor
    cur = connection.cursor()
    cur2 = connection.cursor()
    # "ahmed is %s and  %s" % ("Good", "Great")
    # "select * from employee where name =ahmed and age=30"
    # "select * from employee where name =%s and age=%s"
    # "select * from employee where name =%s and age=%s" % tuple(["ahmed",30])
    sql = sql % tuple(params)
    # excute query
    cur.execute(sql)
    # serialize results into JSON
    all_data = cur.fetchall()
    return all_data
