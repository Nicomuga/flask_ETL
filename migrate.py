from flask_migrate import MigrateCommand
from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()

cli = FlaskGroup(create_app=create_app)

# Agregar el comando de migración a Flask CLI
@cli.command('db')
def migrate():
    MigrateCommand(app, db)

if __name__ == '__main__':
    cli()
