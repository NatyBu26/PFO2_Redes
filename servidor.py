# Importar las herramientas para crear la API.
from flask import Flask, request, jsonify, session

# Importar las funciones para proteger y verificar las contraseñas.
from werkzeug.security import generate_password_hash, check_password_hash

# Importar SQLite para trabajar con la base de datos.
import sqlite3

# Importar herramientas para generar una clave secreta aleatoria.
import secrets


# Crear la aplicación Flask.
app = Flask(__name__)

# Mostrar las letras con tilde y la ñ directamente en las respuestas JSON.
app.json.ensure_ascii = False

# Indicar que las respuestas JSON utilizan la codificación UTF-8.
app.json.mimetype = "application/json; charset=utf-8"

# Configurar la clave para firmar las cookies de sesión.
app.config["SECRET_KEY"] = secrets.token_hex(32)


# Crear la base de datos y la tabla de usuarios si no existen.
def inicializar_bd():
    conexion = sqlite3.connect("usuarios.db")

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY,
                usuario TEXT NOT NULL UNIQUE,
                contrasena_hash TEXT NOT NULL
            )
        """)

        conexion.commit()

    finally:
        conexion.close()


# Guardar un usuario con su contraseña protegida mediante hash.
def guardar_usuario(usuario, contrasena):
    contrasena_hash = generate_password_hash(contrasena)
    conexion = sqlite3.connect("usuarios.db")

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            INSERT INTO usuarios (usuario, contrasena_hash)
            VALUES (?, ?)
        """, (usuario, contrasena_hash))

        conexion.commit()
        return True

    except sqlite3.IntegrityError:
        return False

    finally:
        conexion.close()


# Recibir y validar los datos para registrar un usuario.
@app.route("/registro", methods=["POST"])
def registrar_usuario():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Debe enviar un objeto JSON."}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contrasena, str):
        return jsonify({
            "error": "El usuario y la contraseña deben ser textos."
        }), 400

    usuario = usuario.strip()

    if not usuario or not contrasena.strip():
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios."
        }), 400

    if guardar_usuario(usuario, contrasena):
        return jsonify({
            "mensaje": "Usuario registrado correctamente."
        }), 201

    return jsonify({"error": "El usuario ya existe."}), 409


# Buscar un usuario por su nombre en la base de datos.
def buscar_usuario(usuario):
    conexion = sqlite3.connect("usuarios.db")

    try:
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, usuario, contrasena_hash
            FROM usuarios
            WHERE usuario = ?
        """, (usuario,))

        return cursor.fetchone()

    finally:
        conexion.close()


# Verificar las credenciales e iniciar la sesión del usuario.
@app.route("/login", methods=["POST"])
def iniciar_sesion():
    datos = request.get_json(silent=True)

    if not isinstance(datos, dict):
        return jsonify({"error": "Debe enviar un objeto JSON."}), 400

    usuario = datos.get("usuario")
    contrasena = datos.get("contraseña")

    if not isinstance(usuario, str) or not isinstance(contrasena, str):
        return jsonify({
            "error": "El usuario y la contraseña deben ser textos."
        }), 400

    usuario = usuario.strip()

    if not usuario or not contrasena.strip():
        return jsonify({
            "error": "El usuario y la contraseña son obligatorios."
        }), 400

    usuario_encontrado = buscar_usuario(usuario)

    if usuario_encontrado is None:
        return jsonify({
            "error": "Usuario o contraseña incorrectos."
        }), 401

    if not check_password_hash(usuario_encontrado[2], contrasena):
        return jsonify({
            "error": "Usuario o contraseña incorrectos."
        }), 401

    session.clear()
    session["usuario_id"] = usuario_encontrado[0]

    return jsonify({"mensaje": "Inicio de sesión exitoso."}), 200  


# Mostrar la bienvenida únicamente a usuarios con sesión iniciada.
@app.route("/tareas", methods=["GET"])
def mostrar_tareas():
    if "usuario_id" not in session:
        return jsonify({
            "error": "Debe iniciar sesión para acceder."
        }), 401

    return """
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <title>Bienvenida</title>
        </head>
        <body>
            <h1>¡Bienvenido al sistema de gestión de tareas!</h1>
            <p>Iniciaste sesión correctamente.</p>
        </body>
        </html>
    """, 200


# Preparar la base de datos e iniciar el servidor.
if __name__ == "__main__":
    inicializar_bd()
    app.run(host="127.0.0.1", port=5000)