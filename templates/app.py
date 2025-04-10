from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)

# Crear conexión a SQLite
def create_connection():
    try:
        connection = sqlite3.connect("submissions.db")
        return connection
    except sqlite3.Error as e:
        print(f"Error de conexión: '{e}'")
        return None

# Crear tabla si no existe
def create_table():
    connection = create_connection()
    if connection:
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS submissions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                email TEXT,
                design TEXT,
                pages TEXT,
                message TEXT
            )
        ''')
        connection.commit()
        cursor.close()
        connection.close()

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
            VALUES (?, ?, ?, ?, ?)
        ''', (name, email, design, pages, message))
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"status": "success", "message": "Datos guardados correctamente"}), 200
    except sqlite3.Error as e:
        print(f"Error al insertar: '{e}'")
        return jsonify({"status": "error", "message": "No se pudo insertar en la base de datos"}), 500

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
