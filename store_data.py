import sqlite3
import json
import os

def migrate_fn_for_json_to_sqlite():
    base_path = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(base_path,'users.json')

    with open(json_path,'r') as f:
        users = json.load(f)

    conn = sqlite3.connect('users_db.db')
    cursor = conn.cursor()

    cursor.execute('''
                   CREATE TABLE IF NOT EXISTS users (
                   id INTEGER PRIMARY KEY,
                   first_name TEXT,
                   last_name TEXT,
                   company_name TEXT,
                   age INTEGER,
                   city TEXT,
                   state TEXT,
                   zip TEXT,
                   email TEXT,
                   web TEXT
                   )''')
    
    for user in users:
        cursor.execute('''
                       INSERT OR REPLACE INTO users (id, first_name, last_name, company_name, age, city, state, zip, email, web)
                       VALUES (?,?,?,?,?,?,?,?,?,?)''',
                       (user['id'], user['first_name'], user['last_name'], user['company_name'], user['age'], user['city'], user['state'], user['zip'], user['email'], user['web'])
                       )
        
    conn.commit()
    conn.close()
    print("Data stored in DB!")

if __name__ == "__main__":
    migrate_fn_for_json_to_sqlite()