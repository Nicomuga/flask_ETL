import os
import logging
from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context
from dotenv import load_dotenv
from flask import current_app
from app import create_app, db

# Cargar las variables de entorno desde .env
load_dotenv()

# Configurar el logging para Alembic
config = context.config
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


# Función para obtener el motor de la base de datos desde Flask
def get_engine():
    try:
        # Este método funciona con Flask-SQLAlchemy<3 y Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # Este método funciona con Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


# Función para obtener la URL del motor de la base de datos
def get_engine_url():
    try:
        # Renderizar la URL como una cadena, ocultando la contraseña si está presente
        return get_engine().url.render_as_string(hide_password=False).replace('%', '%%')
    except AttributeError:
        # Si no se puede renderizar como cadena, convertir a cadena y reemplazar los signos de porcentaje
        return str(get_engine().url).replace('%', '%%')


# Configurar la URL de SQLAlchemy en la configuración de Alembic
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db


# Función para obtener los metadatos de la base de datos
def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


# Función para ejecutar migraciones en modo offline
def run_migrations_offline():
    # Obtener la URL de la base de datos desde la configuración
    url = config.get_main_option("sqlalchemy.url")
    # Configurar Alembic con la URL de la base de datos y los metadatos
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )
    # Ejecutar las migraciones dentro de una transacción
    with context.begin_transaction():
        context.run_migrations()


# Función para ejecutar migraciones en modo online
def run_migrations_online():
    # Callback para procesar las directivas de revisión
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    # Obtener los argumentos de configuración para Alembic desde Flask-Migrate
    conf_args = current_app.extensions['migrate'].configure_args
    # Si no hay un callback definido para procesar las directivas de revisión, agregarlo
    if conf_args.get("process_revision_directives") is None:
        conf_args["process_revision_directives"] = process_revision_directives

    # Obtener el motor de la base de datos
    connectable = get_engine()

    # Conectar al motor de la base de datos
    with connectable.connect() as connection:
        # Configurar Alembic con la conexión, los metadatos y los argumentos de configuración
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **conf_args
        )

        # Ejecutar las migraciones dentro de una transacción
        with context.begin_transaction():
            context.run_migrations()


# Determinar si Alembic está en modo offline u online y ejecutar las migraciones correspondientes
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
