import mysql.connector
from mysql.connector import Error
from flask import Flask, redirect, render_template, request, url_for, session, jsonify
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

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username:
            cursor.execute("SELECT user_id, password FROM login_info WHERE username=%s", (username,))
            user = cursor.fetchone()

            if user:
                user_id, stored_password = user
                if hashlib.sha256(password.encode()).hexdigest() == stored_password:
                    session['user_id'] = user_id
                    session['username'] = username
                    return redirect(url_for('home'))
                else:
                    return render_template('login.html', message='Invalid password')
            else:
                return render_template('login.html', message='Invalid username')
    
    return render_template("login.html")

@app.route('/create_user', methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        new_username = request.form["new_username"]
        new_password = request.form["new_password"]
        
        if new_password!="":

            hashed_password = hashlib.sha256(new_password.encode()).hexdigest()


            if new_username and new_username != new_password:
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
                return render_template('create_user.html',messsage="same username and password")
        else:
            return render_template('create_user.html',message="invalid password")
    
    return render_template('create_user.html')

@app.route('/home', methods=["GET"])
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('home.html')

@app.route('/create_student', methods=["POST"])
def create_student():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    dob = request.form["dob"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    address = request.form["address"]
    user_id = session['user_id']
    
    cursor.execute("SELECT * FROM student_info where email=%s",(email,))
    existing_user_email=cursor.fetchone()
    
    if existing_user_email:
        return render_template('home.html',message="email already exists")
        
    
    else:

        cursor.execute(
            "INSERT INTO student_info (first_name, last_name, dob, email, phone_number, address, user_id) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (first_name, last_name, dob, email, phone_number, address, user_id)
        )
        connection.commit()
        return render_template('home.html',message="student added sucessfully")

@app.route('/view_students', methods=["GET"])
def view_students():
    cursor.execute("SELECT * FROM student_info")
    students = cursor.fetchall()
    return render_template('view_students.html', students=students)

@app.route('/update_student/<int:student_id>', methods=["POST"])
def update_student(student_id):
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    dob = request.form["dob"]
    email = request.form["email"]
    phone_number = request.form["phone_number"]
    address = request.form["address"]

    cursor.execute(
        "UPDATE student_info SET first_name=%s, last_name=%s, dob=%s, email=%s, phone_number=%s, address=%s "
        "WHERE student_id=%s",
        (first_name, last_name, dob, email, phone_number, address, student_id)
    )
    connection.commit()
    return redirect(url_for('view_students', message="updated sucessfully"))

@app.route('/delete_student/<int:student_id>', methods=["POST"])
def delete_student(student_id):
    cursor.execute("DELETE FROM student_info WHERE student_id=%s", (student_id,))
    connection.commit()
    return redirect(url_for('view_students', message="updated sucessfully"))


@app.route('/logout',methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
