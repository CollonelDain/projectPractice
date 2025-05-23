import sqlite3  

connection = sqlite3.connect('db.sqlite3')  
cursor = connection.cursor()  

#cursor.execute('INSERT INTO scientists_category (id, name) VALUES (?, ?)', (2, 'Математика'))
'''
cursor.execute('SELECT * FROM sqlite_master where type="table";')
tables = cursor.fetchall()
for tb in tables:
    print(tb)
'''
cursor.execute('SELECT * FROM scientists_category')
cats = cursor.fetchall()
for cat in cats:
    print(cat)

connection.commit()
connection.close()