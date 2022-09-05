import sqlite3

def create_schema():
    connection = sqlite3.connect('Competency.db')
    cursor = connection.cursor()
    with open('create_db.txt','rt') as schema:
        queries = schema.readlines()
        
        for query in queries:
            cursor.execute(query)
        connection.commit()

create_schema()
