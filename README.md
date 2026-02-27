User Management API

A lightweight REST API built with Flask and SQLite. This project allows you to manage user data (CRUD operations) and includes features like pagination, searching, and sorting.

Prerequisites
    1. Python 3.x (Installed on your Mac)
    2. Flask library

Setup & Installation
    1. Install Flask
        Open your terminal in VS Code and run: 
            pip3 install flask
    2. Initialize the Database
        Before running the API, you need to migrate the data from your users.json file into the SQLite database (users_db.db): 
            python3 store_data.py

        This script handles the FileNotFoundError by using absolute paths and prevents KeyError by using the .get() method.
    3. Running the API
        Start the server by running: 
            python3 test.py

        Keep this terminal open. The API will be running at http://127.0.0.1:5000.

Project Structure

test.py: The main Flask application containing your GET, POST, PUT, PATCH, and DELETE routes.

store_data.py: Migration script to read users.json and populate the database.

users_db.db: The SQLite database file created after migration.

users.json: The source file containing 20 dummy user records.

Testing Endpoints

Since Postman isn't installed, use the REST Client extension in VS Code with a .http file or use
curl in a new terminal window.
Examples:

Get All (Paginated): GET http://127.0.0.1:5000/todos?limit=5&page=1
Search Name: GET http://127.0.0.1:5000/todos?search=Sneha
Get by ID: GET http://127.0.0.1:5000/todos/14
Post: POST http://127.0.0.1:5000/users
      {
        "first_name": "Hardik",
        "last_name": "Himanshu Pandya",
        "company_name": "MI",
        "age": 33,
        "city": "Mumbai",
        "state": "Maharastra",
        "zip": "625005",
        "email": "hardik@mi.com",
        "web": "https://mi_blog.com"
      }
Put: PUT http://127.0.0.1:5000/users/16
     {
        "first_name": "Sneha",
        "last_name": "Suresh",
        "company_name": "TCE",
        "age": 22,
        "city": "Kkdi",
        "state": "TN",
        "zip": "625015",
        "email": "sneha@example.com",
        "web": "https://sneha.com"
     }
Patch: PATCH http://127.0.0.1:5000/users/16
       {
        "company_name": "JuniperNetworks"
       }
Delete User: DELETE http://127.0.0.1:5000/users/2
Get statistics: GET http://127.0.0.1:5000/api/users/summary

Notes on Database Logic

Parameterized Queries: All routes use the (id,) tuple syntax to prevent SQL injection.

Row Factory: The database uses sqlite3.Row to return data as dictionaries instead of tuples for better JSON compatibility.

Auto-Increment: New users created via POST automatically receive the next available ID using cursor.lastrowid