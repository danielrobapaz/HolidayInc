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
bp = Blueprint('userView', __name__, url_prefix='/root')

@bp.route('/users', methods=('GET', 'POST'))
@root_required
def userView():
    db = get_db()

    if request.method == 'POST':
        if 'create' in request.form:
            return redirect(url_for('userView.createUser'))
        
        elif 'modify-user' in request.form:
            session['modify_user'] = request.form['modify-user']
            return redirect(url_for('modifyUser.modifyUser'))
    
    users = db.execute(
        """SELECT 
            u.id as id, 
            u.username as username, 
            u.firstname as firstname, 
            u.secondname as secondname, 
            r.name as role, 
            p.description as proyect, 
            u.auth as auth
           FROM user u
           INNER JOIN roles r ON u.roleId = r.id
           INNER JOIN proyect p ON u.proyId = p.id 
           WHERE u.id != 0"""
    ).fetchall()

    areProyects = db.execute(
        """SELECT * FROM proyect"""
    ).fetchall() != []

    return render_template('index/root/userView.html', users=users, areProyects=areProyects)

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
                    """INSERT INTO user (username, firstname, secondname, password, roleId, proyId, auth) 
                     VALUES (?, ?, ?, ?, ?, ?, ?)""",
                    (username, firstname, secondname, generate_password_hash(password), role, proyect, 1)
                )
                utilities.loggerQuery(db, g.user['username'], 'createUser', username)
                utilities.loggerQuery(db, g.user['username'], 'setRole', [username, role])
                utilities.loggerQuery(db, g.user['username'], 'setProyect', [username, proyect])

                db.commit()

            except db.IntegrityError:
                error = f"User \'{username}\' is already registered."

            else:
                # the user was registered, redirect to login view
                return redirect(url_for("user.root"))

        flash(error) # show any error that happened

    proyects = db.execute(
        """SELECT 
            id, 
            description 
           FROM proyect""",
    ).fetchall()

    roles = db.execute(
        """SELECT 
            id,
            name 
           FROM roles
           WHERE id != 1"""
    ).fetchall()

    return render_template('index/root/createUser.html', proyects = proyects, roles = roles)