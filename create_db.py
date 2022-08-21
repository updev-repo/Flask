import mysql.connector
my_db = mysql.connector.connect(
    host='localhost',
    passwd='1122',
    user='root'
)
my_crusor = my_db.cursor()
my_crusor.execute('create database flask')
my_crusor.execute('show databases')
for db in my_crusor:
    print(db)
