import pymysql
connection = pymysql.connect(host='localhost',
                             user='root',
                             port='3306',
                             password='')

try:
    with connection.cursor() as cursor:
        cursor.execute('CREATE DATABASE rasadatabase')
       # cursor.execute('create table ')
 
finally:
    connection.close()