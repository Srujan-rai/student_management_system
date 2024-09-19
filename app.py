import mysql.connector
from mysql.connector import Error
from flask import Flask,redirect,render_template,Response,request


def create_connection():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            database='student_management_system',
            user='root',
            password='8861203688'
        )
        if connection.is_connected():
            print("database connected sucessfully")
            return connection
    except Error as e:
        print(f"error{str(e)}")
        return None


connection=create_connection()


cursor=connection.cursor()
    