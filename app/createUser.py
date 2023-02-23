# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from app.auth import root_required
from app.db import get_db
from . import utilities

# creates a blueprint named 'createUser'. A blueprint is a way
# to organize a group of related views.
bp = Blueprint('createUser', __name__)


@bp.route('/createUser', methods=('GET', 'POST'))
@root_required
def createUser():
    db = get_db()
    if request.method == "POST":
        # request for the input 
        username = request.form['username']
        firstname = request.form['firstname']
        secondname = request.form['secondname']
        password = request.form['password']
        role = request.form['role']
        proyect = request.form['proyect']

        error = None

        if not username:
            error = 'Username is required.'
        elif not firstname:
            error = 'First name is required.'
        elif not secondname:
            error = 'Second name is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # insert a new user to the user table in the database
                db.execute(
                    "INSERT INTO user (username, firstname, secondname, password, role, proyId, auth) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (username, firstname, secondname, generate_password_hash(password), role, proyect, 1)
                )
                utilities.loggerQuery(db, 'admin', 'createUser', username)
                utilities.loggerQuery(db, 'admin', 'setRole', [username, role])
                utilities.loggerQuery(db, 'admin', 'setProyect', [username, proyect])

                db.commit()

            except db.IntegrityError:
                error = f"User \'{username}\' is already registered."

            else:
                # the user was registered, redirect to login view
                return redirect(url_for("user.root"))

        flash(error) # show any error that happened

    proyects = db.execute(
        'SELECT id, description FROM proyect',
    ).fetchall()

    return render_template('index/root/createUser.html', proyects = proyects)