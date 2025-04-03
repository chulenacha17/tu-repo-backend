from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)

# Conectar a MySQL local (XAMPP)
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',  # Si le pusiste contraseña a MySQL en Workbench, colócala aquí
            database='mydb'
        )
        return connection
    except Error as e:
        print(f"Error de conexión: '{e}'")
        return None

@app.route('/api/send', methods=['POST'])
def submit_form():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    design = data.get('design')
    pages = data.get('pages')
    message = data.get('message')

    connection = create_connection()
    if connection is None:
        return jsonify({"status": "error", "message": "No se pudo conectar a la base de datos"}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('''
            INSERT INTO submissions (name, email, design, pages, message)
            VALUES (%s, %s, %s, %s, %s)
        ''', (name, email, design, pages, message))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Datos guardados correctamente"}), 200
    except Error as e:
        print(f"Error al insertar: '{e}'")
        return jsonify({"status": "error", "message": "No se pudo insertar en la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
