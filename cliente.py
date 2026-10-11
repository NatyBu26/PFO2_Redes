# Importar las herramientas para enviar solicitudes HTTP al servidor.
import requests

# Importar la función para ingresar la contraseña sin mostrarla en pantalla.
from getpass import getpass


# Definir la dirección del servidor.
URL_SERVIDOR = "http://127.0.0.1:5000"

# Crear una sesión para conservar las cookies entre las solicitudes.
sesion = requests.Session()


# Solicitar el usuario y la contraseña para enviarlos a la API.
def pedir_credenciales():
    usuario = input("Usuario: ").strip()
    contrasena = getpass("Contraseña: ")

    return {
        "usuario": usuario,
        "contraseña": contrasena
    }


# Mostrar el código HTTP y el mensaje recibido del servidor.
def mostrar_respuesta(respuesta):
    print(f"\nCódigo HTTP: {respuesta.status_code}")

    try:
        datos = respuesta.json()
        mensaje = datos.get("mensaje") or datos.get("error")
        print(mensaje if mensaje else datos)
    except ValueError:
        print(respuesta.text)


# Solicitar los datos y enviarlos al servidor para registrar un usuario.
def registrar_usuario():
    datos = pedir_credenciales()

    try:
        respuesta = sesion.post(
            f"{URL_SERVIDOR}/registro",
            json=datos,
            timeout=10
        )
        mostrar_respuesta(respuesta)
    except requests.exceptions.Timeout:
        print("\nEl servidor tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print("\nNo se pudo conectar con el servidor.")
    except requests.exceptions.RequestException:
        print("\nOcurrió un error al enviar la solicitud.")


# Verificar las credenciales y conservar la cookie de sesión del servidor.
def iniciar_sesion():
    datos = pedir_credenciales()

    # Borrar las cookies anteriores antes de intentar un nuevo login.
    sesion.cookies.clear()

    try:
        respuesta = sesion.post(
            f"{URL_SERVIDOR}/login",
            json=datos,
            timeout=10
        )
        mostrar_respuesta(respuesta)
    except requests.exceptions.Timeout:
        print("\nEl servidor tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print("\nNo se pudo conectar con el servidor.")
    except requests.exceptions.RequestException:
        print("\nOcurrió un error al enviar la solicitud.")


# Solicitar la bienvenida utilizando la cookie de sesión si está disponible.
def acceder_tareas():
    try:
        respuesta = sesion.get(
            f"{URL_SERVIDOR}/tareas",
            timeout=10
        )
        mostrar_respuesta(respuesta)
    except requests.exceptions.Timeout:
        print("\nEl servidor tardó demasiado en responder.")
    except requests.exceptions.ConnectionError:
        print("\nNo se pudo conectar con el servidor.")
    except requests.exceptions.RequestException:
        print("\nOcurrió un error al enviar la solicitud.")


# Mostrar el menú y ejecutar la opción elegida por el usuario.
def mostrar_menu():
    while True:
        print("\n--- Sistema de gestión de tareas ---")
        print("1. Registrar usuario.")
        print("2. Iniciar sesión.")
        print("3. Acceder a tareas.")
        print("4. Salir.")

        opcion = input("Elegí una opción: ").strip()

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            iniciar_sesion()
        elif opcion == "3":
            acceder_tareas()
        elif opcion == "4":
            print("\nHasta luego.")
            break
        else:
            print("\nOpción inválida. Ingresá un número del 1 al 4.")


# Iniciar el cliente y cerrar sus conexiones al finalizar.
if __name__ == "__main__":
    try:
        mostrar_menu()
    except KeyboardInterrupt:
        print("\nCliente cerrado por el usuario.")
    finally:
        sesion.close()