# PFO2 - Sistema de Gestión de Tareas con API y Base de Datos

Proyecto realizado para la materia Programación sobre Redes del IFTS 29.

El sistema permite registrar usuarios, iniciar sesión y acceder a una página de bienvenida mediante una API desarrollada con Flask. Los usuarios se almacenan en una base de datos SQLite y las contraseñas se guardan como hashes.

También incluye un cliente de consola que permite interactuar con la API mediante un menú de opciones.

## Tecnologías utilizadas

- Python.
- Flask.
- SQLite.
- Werkzeug para generar y verificar hashes de contraseñas.
- Requests para enviar solicitudes HTTP desde el cliente.

## Archivos del proyecto

- `servidor.py`: API con registro de usuarios, inicio de sesión y acceso protegido a la bienvenida. Incluye la creación y las consultas de la base de datos.
- `cliente.py`: cliente de consola con un menú para interactuar con la API.
- `requirements.txt`: dependencias necesarias para ejecutar el proyecto.
- `.gitignore`: archivos y carpetas que se excluyen del repositorio.
- `README.md`: descripción del proyecto e instrucciones de instalación y uso.
- `docs/PFO2_Documentacion_de_pruebas.pdf`: documento con los procedimientos, resultados y las 16 evidencias.
- `docs/capturas/`: imágenes originales de las pruebas realizadas.

La base de datos `usuarios.db` se crea automáticamente al ejecutar el servidor por primera vez. Se conserva localmente y se excluye del repositorio.

## Instalación

Se necesita tener Python instalado.

Abrir una terminal de PowerShell en la carpeta del proyecto y crear un entorno virtual:

```powershell
python -m venv .venv
```

Instalar las dependencias utilizando el Python del entorno virtual:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Los comandos de ejecución siguientes utilizan directamente el entorno virtual, por lo que no es necesario activarlo.

## Ejecución

### Iniciar el servidor

En una terminal de PowerShell, ubicada en la carpeta del proyecto, ejecutar:

```powershell
.\.venv\Scripts\python.exe servidor.py
```

El servidor queda disponible en `http://127.0.0.1:5000`. Mantener esta terminal abierta mientras se utiliza el cliente.

### Iniciar el cliente

Abrir una segunda terminal de PowerShell en la misma carpeta y ejecutar:

```powershell
.\.venv\Scripts\python.exe cliente.py
```

El cliente muestra las siguientes opciones:

1. Registrar usuario.
2. Iniciar sesión.
3. Acceder a tareas.
4. Salir.

Para probar el recorrido completo, registrar un usuario, iniciar sesión con sus credenciales y acceder a tareas. Esta última opción muestra el HTML de bienvenida recibido del servidor.

Al ingresar la contraseña, los caracteres no se muestran en pantalla.

### Finalizar

Elegir la opción 4 para cerrar el cliente. Para detener el servidor, presionar `Ctrl + C` en su terminal.

## Rutas de la API

| Método | Ruta | Función |
| --- | --- | --- |
| POST | `/registro` | Registrar un usuario y guardar el hash de su contraseña. |
| POST | `/login` | Verificar las credenciales e iniciar una sesión. |
| GET | `/tareas` | Devolver el HTML de bienvenida si existe una sesión autenticada. |

Las rutas `/registro` y `/login` reciben un objeto JSON con este formato:

```json
{
  "usuario": "usuario_prueba",
  "contraseña": "1234"
}
```

Estos valores son un ejemplo para realizar pruebas.

### Códigos de respuesta HTTP

| Código | Situación |
| --- | --- |
| 200 | Inicio de sesión o acceso a la bienvenida exitosos. |
| 201 | Usuario registrado correctamente. |
| 400 | Datos incompletos, tipos incorrectos o cuerpo JSON inválido. |
| 401 | Credenciales incorrectas o acceso sin sesión. |
| 409 | Intento de registrar un usuario que ya existe. |

El cliente conserva la cookie de sesión para acceder a `/tareas` después del login. Antes de cada nuevo intento de login, borra las cookies anteriores.

Al reiniciar el servidor, las sesiones anteriores dejan de ser válidas y es necesario iniciar sesión nuevamente. Los usuarios permanecen guardados en SQLite.

## Pruebas realizadas

Se documentaron 16 evidencias de ejecución de la API y del cliente de consola.

Las pruebas incluyen registro e inicio de sesión, acceso con y sin autenticación, usuario repetido, contraseña incorrecta, datos incompletos y persistencia después de reiniciar el servidor.

También se verificaron el menú del cliente, el ingreso de una opción inválida, el manejo del servidor detenido y la salida del programa.

- [Consultar la documentación de pruebas](docs/PFO2_Documentacion_de_pruebas.pdf).
- [Ver las capturas originales](docs/capturas/).

## Respuestas conceptuales

### ¿Por qué hashear contraseñas?

Las contraseñas se hashean para evitar guardarlas en texto plano. Si alguien accede a la base de datos, no encuentra directamente las contraseñas originales de los usuarios.

El hash es una transformación de una sola vía: no está diseñado para recuperar la contraseña original. Al iniciar sesión, se verifica si la contraseña ingresada corresponde al hash almacenado.

En este proyecto se utiliza `generate_password_hash` de Werkzeug para generar el hash y `check_password_hash` para verificar la contraseña durante el login.

El uso de hashes adecuados dificulta los intentos de adivinar las contraseñas, aunque no elimina todos los riesgos.

### Ventajas de usar SQLite en este proyecto

SQLite permite almacenar los usuarios de forma persistente: los datos se conservan aunque se detenga o reinicie el servidor.

Es adecuado para este proyecto porque:

- No requiere instalar ni configurar un servidor de base de datos independiente.
- Guarda la base de datos en un archivo local, lo que facilita su manejo.
- Python incluye el módulo `sqlite3`, que permite trabajar con SQLite.
- Permite utilizar consultas SQL y restricciones, como `UNIQUE`, para evitar usuarios repetidos.
- Ofrece transacciones para confirmar los cambios realizados en la base de datos.

Por estas características, SQLite resulta una opción sencilla para una aplicación local de este tamaño.