# Proyecto Flask

Este proyecto es una aplicación Flask que se utiliza para extraer datos de Google Drive (originalmente era de sharepoint de microsoft) y guardarlos en una base de datos PostgreSQL. La aplicación utiliza blueprints para organizar las diferentes partes de la API.

## Estructura del proyecto

El proyecto tiene la siguiente estructura de archivos:

```
flask_app
├── .env
├── app
│   ├── __init__.py
│   ├── config.py
│   ├── models.py
    ├── drive.py    
│   ├── sharepoint.py
│   ├── views.py
├── migrations
├── app.py
├── requirements.txt
└── README.md
```

- `.env`: Este archivo contiene las variables de entorno necesarias para la configuración de la aplicación Flask, como el nombre de usuario y contraseña de SharePoint, la URL del sitio, la URL de la carpeta base, las credenciales de la base de datos PostgreSQL y la configuración de Flask.

- `app/__init__.py`: Este archivo es el punto de entrada de la aplicación Flask. Crea una instancia de la aplicación Flask, configura la base de datos SQLAlchemy y registra los blueprints de las vistas.

- `app/config.py`: Este archivo contiene la configuración de la aplicación Flask, incluyendo la URL de la base de datos PostgreSQL.

- `app/models.py`: Este archivo define los modelos de datos de la aplicación Flask. Contiene la definición de la clase `MontoError` y  `OtrosCampos` que representan 2 tablas en la base de datos.

- `app/drive.py`: Este archivo contiene funciones para interactuar con SharePoint. Incluye una función `fetch_data_from_google_drive` que obtiene .xlxs y los devuelve como un DataFrame de pandas. 

- `app/views.py`: Este archivo define los endpoint de la aplicación Flask. Incluye un endpoint `fetch` que utiliza la función `fetch_data` para obtener datos de drive y guardarlos en la base de datos.

- `migrations/`: Este directorio se utiliza para almacenar las migraciones de la base de datos generadas por Flask-Migrate.

- `manage.py`: Este archivo se utiliza para ejecutar la aplicación Flask y las migraciones de la base de datos. Importa la función `create_app` del archivo `app/__init__.py` y crea una instancia de la aplicación Flask.

- `requirements.txt`: Este archivo contiene las dependencias del proyecto.

## Configuración y ejecución

Sigue los pasos a continuación para configurar y ejecutar la aplicación Flask:

1. Instala las dependencias del proyecto ejecutando el siguiente comando en la terminal:

   ```
   pip install -r requirements.txt
   ```
      Si por alguna razón requirements.txt no se encuentra actualizado. Siempre puedes hacer 
      
      ```
      pip install pipreqs
      ```
      Y luego:
      ```
      pipreqs --force
      ```
      esto para reescribir el requirements.txt

2. Configura pipreqs . --force
as variables de entorno en el archivo `.env` con los valores adecuados. Asegúrate de proporcionar los siguientes valores:

   ```
   POSTGRES_USER=postgres
   POSTGRES_PASSWORD=
   POSTGRES_DB=
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   FLASK_APP=app.py
   FLASK_ENV=development
   GOOGLE_DRIVE_CREDENTIALS_FILE=get it from drive and put it in your root
   GOOGLE_DRIVE_FOLDER_ID= get it from your drive 
   ```

3. Ejecuta las migraciones de la base de datos ejecutando el siguiente comando en la terminal:

   ```
   python manage.py db upgrade  --or just--  flask db upgrade --and later-- flask db migrate -m 'message here'
   ```

4. Ejecuta la aplicación Flask ejecutando el siguiente comando en la terminal:

   ```
   python manage.py run --or-- flask run
   ```

   La aplicación Flask estará disponible en `http://localhost:5000`.



Este proyecto es una base sólida para construir una API que utiliza blueprints en Flask. Puedes agregar nuevos archivos en el directorio `app` para cada blueprint y definir las rutas y funciones de controlador correspondientes en cada archivo. Luego, registra los blueprints en el archivo `app/__init__.py` para que sean utilizados por la aplicación Flask.