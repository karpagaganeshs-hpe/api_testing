import sqlite3
from flask import Flask, jsonify, request #flask - library Flask - class

app = Flask(__name__) #create a new flask application, using that app we will configure our api.

def get_db_connection():
    #now connecting to db connected by running store_data.py
    conn = sqlite3.connect('users_db.db')
    #default rtn type of sqlite3 is tuples row_factory converts it to rtn rows that look like dict
    conn.row_factory = sqlite3.Row
    return conn

#now creating a endpoint with  route
#def get_users():
    conn = get_db_connection()
    users_indices = conn.execute('SELECT * FROM users').fetchall()
    conn.close()

    response = [dict(row) for row in users_indices] #takes that row and typecasts it to dict
    return jsonify(response) #takes python dict n converts it to json strings

@app.route("/users", methods = ["GET"])
def get_users():

    limit = request.args.get('limit',default=5,type=int)
    page = request.args.get('page', default=1,type=int)
    search = request.args.get('search', default="",type=str)
    sortby = request.args.get('sort',default='id',type=str)

    offset = (page-1)*limit

    query = "SELECT * FROM users WHERE (first_name LIKE ? OR last_name LIKE ?)"
    params = [f"%{search}%",f"%{search}"]

    cols = ['id','first_name','last_name','age','city']
    if sortby not in cols:
        sortby = "id"

    query += f" ORDER BY {sortby} DESC"

    query += " LIMIT ? OFFSET ?"
    params.extend([limit,offset])
    
    conn = get_db_connection()
    users_indices = conn.execute(query,params).fetchall()
    conn.close()

    response = [dict(row) for row in users_indices] #takes that row and typecasts it to dict
    return jsonify(response) #takes python dict n converts it to json strings

@app.route("/users/<int:id>", methods = ["GET"]) #<> is the dynamic part of the url
def get_user(id):
    conn = get_db_connection()
    user_row = conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()
    conn.close()

    if user_row is None:
        return {"error": "user not found"},404
    
    return jsonify(dict(user_row))

@app.route("/users", methods = ["POST"])
def post_user():
    request_data = request.get_json()

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('''
                       INSERT INTO users (first_name, last_name, company_name, age, city, state, zip, email, web)
                       VALUES (?,?,?,?,?,?,?,?,?)''',
                       (
                           request_data.get('first_name'),
                           request_data.get('last_name'),
                           request_data.get('company_name'),
                           request_data.get('age'),
                           request_data.get('city'),
                           request_data.get('state'),
                           request_data.get('zip'),
                           request_data.get('email'),
                           request_data.get('web'),
                       )
                       )
    
    new_id = cursor.lastrowid #tells what new id is assigned to the user

    conn.commit() #to store permanently in the disk
    conn.close() #to free up sys resources

    request_data['id'] = new_id
    return jsonify(request_data), 201

@app.route("/users/<int:id>", methods = ["PUT"])
def update_user(id):
    request_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    user= conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        conn.close()
        return {"error": "user not found"},404
    
    cursor.execute('''
                   UPDATE users SET first_name = ?, last_name =?, company_name=?, age=?, city=?,state=?,zip=?,email=?,web=? where id = ?''',
                   (
                           request_data.get('first_name' , user['first_name']),
                           request_data.get('last_name', user['last_name']),
                           request_data.get('company_name', user['company_name']),
                           request_data.get('age', user['age']),
                           request_data.get('city', user['city']),
                           request_data.get('state', user['state']),
                           request_data.get('zip', user['zip']),
                           request_data.get('email', user['email']),
                           request_data.get('web', user['web']), id
                       ))
    
    conn.commit()

    updated_user = conn.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    conn.close()

    return jsonify(dict(updated_user))


@app.route("/users/<int:id>", methods = ["DELETE"])
def delete_user(id):
    request_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    user= conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        conn.close()
        return {"error": "user not found"},404
    
    cursor.execute('DELETE FROM users WHERE id=?', (id,))

    conn.commit()
    conn.close()

    return {"message": f"user with id {id} deleted."}

@app.route("/users/<int:id>", methods = ["PATCH"])
def patch_user(id):
    request_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()

    user= conn.execute('SELECT * FROM users WHERE id = ?', (id,)).fetchone()

    if user is None:
        conn.close()
        return {"error": "user not found"},404
    
    cursor.execute('''
                   UPDATE users SET first_name = ?, last_name =?, company_name=?, age=?, city=?,state=?,zip=?,email=?,web=? where id = ?''',
                   (
                           request_data.get('first_name' , user['first_name']),
                           request_data.get('last_name', user['last_name']),
                           request_data.get('company_name', user['company_name']),
                           request_data.get('age', user['age']),
                           request_data.get('city', user['city']),
                           request_data.get('state', user['state']),
                           request_data.get('zip', user['zip']),
                           request_data.get('email', user['email']),
                           request_data.get('web', user['web']), id
                       ))
    
    conn.commit()

    updated_user = conn.execute('SELECT * FROM users WHERE id=?', (id,)).fetchone()
    conn.close()

    return jsonify(dict(updated_user))

@app.route("/api/users/summary", methods = ["GET"])
def get_users_summary():
    conn = get_db_connection()

    tot_users = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]

    avg_age =conn.execute('SELECT ROUND(AVG(age),1) FROM users').fetchone()[0]

    conn.close()

    return jsonify({
        "total_users": tot_users,
        "average_age": avg_age
    })

if __name__ == "__main__":
    app.run(debug=True, port=5000) #debug is true for production servers

