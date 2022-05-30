import mysql.connector

def mysqlInstance():
    config = {
        'user': 'root',
        'password': 'root123',
        'port': '3306',
        'host': 'db',
        'database': 'flaskpersistent'
    }
    
    return mysql.connector.connect(**config)
