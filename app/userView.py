# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from app.auth import root_required
from app.db import get_db
from . import utilities
import re

# creates a blueprint named 'createUser'. A blueprint is a way
# to organize a group of related views.
bp = Blueprint('userView', __name__, url_prefix='/root')

@bp.route('/users', methods=('GET', 'POST'))
@root_required
def userView():
    db = get_db()
    flag = False

    if request.method == 'POST':
        if 'create' in request.form:
            return redirect(url_for('userView.createUser'))
        
        elif 'modify-user' in request.form:
            session['modify_user'] = request.form['modify-user']
            return redirect(url_for('modifyUser.modifyUser'))
        
        elif 'aprove' in request.form:
            session['aprove_user'] = request.form['aprove']
            return redirect(url_for('userView.aproveUser'))
        
        elif 'reject' in request.form:
            id = request.form['reject']

            utilities.loggerQuery(db, g.user['username'], 'rejectUser', id)
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()

        elif 'return' in request.form:
            return redirect(url_for('user.root'))
        
        elif 'find-user' in request.form:
            find = request.form['find-user']

            usersToFilter = db.execute(
                """SELECT 
                    u.id as id, 
                    u.username as username, 
                    u.firstname as firstname, 
                    u.secondname as secondname, 
                    r.name as role, 
                    p.description as proyect, 
                    u.auth as auth
                   FROM user u
                   JOIN roles r ON u.roleId = r.id
                   LEFT JOIN proyect p ON u.proyId = p.id 
                   WHERE u.id != 1"""
            ).fetchall()

            usersFiltered = []
            for user in usersToFilter:
                if re.search(find, user['username']) or re.search(find, user['firstname']) or re.search(find, user['secondname']):
                    usersFiltered.append({
                        'id': user['id'],
                        'username': user['username'],
                        'firstname': user['firstname'],
                        'secondname': user['secondname'],
                        'role': user['role'],
                        'proyect': user['proyect'],
                        'auth': user['auth']
                    }) 
            users = usersFiltered
            flag = True
    
    if not flag:
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
               JOIN roles r ON u.roleId = r.id
               LEFT JOIN proyect p ON u.proyId = p.id 
               WHERE u.id != 1"""
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

@bp.route('/aproveUser', methods=('POST', 'GET'))
@root_required
def aproveUser():
    db = get_db()
    proyects = db.execute(
        'SELECT * FROM proyect'
    ).fetchall()

    if request.method == 'POST':
        role = request.form['role']
        proyectId = request.form['proyect']

        # update user role
        db.execute(
            'UPDATE user SET role = ? WHERE id = ?',
            (role, session['aprove_user'],)
        )

        # update user proyectId
        db.execute(
            'UPDATE user SET proyId = ? WHERE id = ?',
            (proyectId, session['aprove_user'],)
        )

        # update user auth
        db.execute(
            'UPDATE user SET auth = 1 WHERE id = ?',
            (session['aprove_user'],)
        )

        # logger querys
        user = db.execute(
            'SELECT username FROM user WHERE id = ?',
            (session['aprove_user'],)   
        ).fetchone()['username']
        
        utilities.loggerQuery(db, 'admin', 'aproveUser', user)
        utilities.loggerQuery(db, 'admin', 'setRole', [user, role])
        utilities.loggerQuery(db, 'admin', 'setProyect', [user, proyectId])

        db.commit()

        return redirect(url_for('user.root'))

    return render_template('index/root/aproveUser.html', proyects = proyects)