import mysql.connector
from mysql.connector import Error
from flask import Flask, redirect, render_template, request, url_for, session, flash,jsonify
import hashlib
import secrets


app = Flask(__name__)

app.secret_key = secrets.token_hex(16)  


def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='student_management_system',
            user='root',
            password='8861203688'
        )
        if connection.is_connected():
            print("Database connected successfully")
            return connection
    except Error as e:
        print(f"Error: {str(e)}")
        return None


connection = create_connection()
cursor = connection.cursor()

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username != '':
            cursor.execute("SELECT user_id, password FROM login_info WHERE username=%s", (username,))
            user = cursor.fetchone()

            if user:
                user_id = user[0]
                stored_password = user[1]

                if hashlib.sha256(password.encode()).hexdigest() == stored_password:
                    # Store user_id in the session
                    session['user_id'] = user_id
                    session['username'] = username
                    return render_template('home.html', message="Welcome to the Student Management System")
                else:
                    return render_template('login.html', message='Invalid password')
            else:
                return render_template('login.html', message='Invalid username')
        else:
            return render_template('login.html', message="Please enter a valid username.")
    
    return render_template("login.html")


@app.route('/create_user', methods=["POST", "GET"])
def create_user():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]

        hashed_password = hashlib.sha256(new_password.encode()).hexdigest()

        if new_username != '' and new_username != new_password:
            try:
                cursor.execute(
                    "INSERT INTO login_info (username, password) VALUES (%s, %s)",
                    (new_username, hashed_password)
                )
                connection.commit()
                return render_template('login.html', message="User created successfully")
            except mysql.connector.IntegrityError:
                return render_template('create_user.html', message='Username already exists')
        else:
            return render_template('create_user.html', message="Invalid entry! Username and password cannot be empty or the same.")
    return render_template('create_user.html')


@app.route('/create_student', methods=["GET", "POST"])
def create_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        dob = request.form["dob"]
        email = request.form["email"]
        phone_number = request.form["phone_number"]
        address = request.form["address"]
        user_id = session['user_id']  # Get user_id from the session

        cursor.execute(
            "INSERT INTO student_info (first_name, last_name, dob, email, phone_number, address, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, dob, email, phone_number, address, user_id)
        )
        connection.commit()
        return render_template("home.html", message="Student added successfully")
    
    return render_template("home.html")


@app.route('/view_students',methods=["POST","GET"])
def view_students():
    cursor.execute("SELECT * FROM student_info")
    students=cursor.fetchall()
    return jsonify({"students":students})

@app.route


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
