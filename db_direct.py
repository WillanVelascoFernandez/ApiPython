import mysql.connector

def get_connection():
    return mysql.connector.connect(
        user='root',
        password='1234',
        host='localhost',
        port=3306,
        database='api'
    )

def read_historial():
    conn = get_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute('SELECT * FROM loteria')
            return cursor.fetchall()
    finally:
        conn.close()