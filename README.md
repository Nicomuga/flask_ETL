# Proyecto Flask

Este proyecto es una aplicación Flask que se utiliza para extraer datos de SharePoint y guardarlos en una base de datos PostgreSQL. La aplicación utiliza blueprints para organizar las diferentes partes de la API.

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

- `app/models.py`: Este archivo define el modelo de datos de la aplicación Flask. Contiene la definición de la clase `DataEntry` que representa una entrada de datos en la base de datos.

- `app/sharepoint.py`: Este archivo contiene funciones para interactuar con SharePoint. Incluye una función `fetch_data_from_sharepoint` que obtiene datos de SharePoint y los devuelve como un DataFrame de pandas.

- `app/views.py`: Este archivo define las vistas de la aplicación Flask. Incluye una vista `fetch_data` que utiliza la función `fetch_data_from_sharepoint` para obtener datos de SharePoint y guardarlos en la base de datos.

- `migrations/`: Este directorio se utiliza para almacenar las migraciones de la base de datos generadas por Flask-Migrate.

- `manage.py`: Este archivo se utiliza para ejecutar la aplicación Flask y las migraciones de la base de datos. Importa la función `create_app` del archivo `app/__init__.py` y crea una instancia de la aplicación Flask.

- `requirements.txt`: Este archivo contiene las dependencias del proyecto. Incluye paquetes como Flask, Flask-SQLAlchemy, Flask-Migrate, psycopg2-binary, python-dotenv, pandas y Office365-REST-Python-Client.

## Configuración y ejecución

Sigue los pasos a continuación para configurar y ejecutar la aplicación Flask:

1. Instala las dependencias del proyecto ejecutando el siguiente comando en la terminal:

   ```
   pip install -r requirements.txt
   ```

2. Configura las variables de entorno en el archivo `.env` con los valores adecuados. Asegúrate de proporcionar los siguientes valores:

   ```
   SHAREPOINT_USERNAME=your_username
   SHAREPOINT_PASSWORD=your_password
   SITE_URL=https://yourcompany.sharepoint.com/sites/yoursite
   BASE_FOLDER_URL=/sites/yoursite/Shared Documents/yourfolder
   POSTGRES_USER=your_postgres_username
   POSTGRES_PASSWORD=your_postgres_password
   POSTGRES_DB=your_database_name
   POSTGRES_HOST=your_postgres_host
   POSTGRES_PORT=your_postgres_port
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

3. Ejecuta las migraciones de la base de datos ejecutando el siguiente comando en la terminal:

   ```
   python manage.py db upgrade
   ```

4. Ejecuta la aplicación Flask ejecutando el siguiente comando en la terminal:

   ```
   python manage.py run
   ```

   La aplicación Flask estará disponible en `http://localhost:5000`.

## Detalles de los archivos y directorios

- `.env`: Este archivo contiene las variables de entorno necesarias para la configuración de la aplicación Flask, como las credenciales de SharePoint y la base de datos PostgreSQL.

- `app/__init__.py`: Este archivo es el punto de entrada de la aplicación Flask. Crea una instancia de la aplicación Flask y configura la base de datos SQLAlchemy.

- `app/config.py`: Este archivo contiene la configuración de la aplicación Flask, incluyendo la URL de la base de datos PostgreSQL.

- `app/models.py`: Este archivo define el modelo de datos de la aplicación Flask. Contiene la definición de la clase `DataEntry` que representa una entrada de datos en la base de datos.

- `app/sharepoint.py`: Este archivo contiene funciones para interactuar con SharePoint. Incluye una función `fetch_data_from_sharepoint` que obtiene datos de SharePoint y los devuelve como un DataFrame de pandas.

- `app/views.py`: Este archivo define las vistas de la aplicación Flask. Incluye una vista `fetch_data` que utiliza la función `fetch_data_from_sharepoint` para obtener datos de SharePoint y guardarlos en la base de datos.

- `migrations/`: Este directorio se utiliza para almacenar las migraciones de la base de datos generadas por Flask-Migrate.

- `manage.py`: Este archivo se utiliza para ejecutar la aplicación Flask y las migraciones de la base de datos.

- `requirements.txt`: Este archivo contiene las dependencias del proyecto.

Este proyecto es una base sólida para construir una API que utiliza blueprints en Flask. Puedes agregar nuevos archivos en el directorio `app` para cada blueprint y definir las rutas y funciones de controlador correspondientes en cada archivo. Luego, registra los blueprints en el archivo `app/__init__.py` para que sean utilizados por la aplicación Flask.