import sqlite3
from werkzeug.security import generate_password_hash
import click

# g is a special objecto that is unique for each request
# g is used to store data that migth be accesed by multiple funcion
# during the request

# current_app points to the flask appliacion handling request 
from flask import current_app, g

# returns the database
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types = sqlite3.PARSE_DECLTYPES
        )

        # makes row works as dictionaries
        g.db.row_factory = sqlite3.Row

    return g.db

# close the database
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


# define a command line command called init-db 
# that calls the init_db function 
@click.command('init-db')
def init_db_command():
    # create the existing data ad create new tables
    init_db()

    # inserting the admin user, this will happen every time the db is initialized
    db = get_db()
    try:
        roles = ['admin',
                 'Waiting',
                 'Gerente de operaciones',
                 'Analista de operaciones', 
                 'Supervisor de mecanica', 
                 'Supervisor de pintura y latoneria', 
                 'Especialista en electricidad']
        
        proyStatus = ['Enabled', 'Closed']

        db.execute(
            """INSERT INTO user (username, firstname, secondname, password, roleId, auth) 
               VALUES (?, ?, ?, ?, ?, ?)""",
            ('root', 'root', 'root', generate_password_hash('root'), 1, 1)
        )

        for role in roles:
            db.execute(
                """INSERT INTO roles (name)
                   VALUES (?)""",
                   (role,)
            )

        for status in proyStatus:
            db.execute(
                """INSERT INTO proyectStatus (name)
                   VALUES (?)""",
                   (status,)
            )

        db.commit()
    except db.IntegrityError:
        pass

    else:
        click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)

    # adds init_db_command that can be called with the flask command
    app.cli.add_command(init_db_command)