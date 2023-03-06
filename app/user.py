from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, flash
)
from app.auth import root_required, manager_required, login_required
from app.db import get_db
from . import utilities
from werkzeug.security import generate_password_hash, check_password_hash


# create the blueprint for the 'user'
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/root', methods=('POST', 'GET'))
@root_required
def root():
    db = get_db()
    find = False
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

    proyects = db.execute(
        """SELECT
            p.id,
            p.description as description,
            p.start as start,
            p.end as end,
            s.name as status
           FROM proyect p
           INNER JOIN proyectStatus s ON p.statusId = s.id"""
    ).fetchall()

    if request.method == 'POST':
        if 'create' in request.form:
            # action of crete a new user button
            return redirect(url_for("createUser.createUser"))

        elif 'proyect' in request.form:
            return redirect(url_for('createProyect.createProyect'))

        elif 'find-user' in request.form:
            user = request.form['find-user']

            if user != "":
                users = db.execute (
                    'SELECT id, username, firstname, secondname, role, proyId, auth FROM user WHERE role != ? AND username = ?',
                    ('admin', user)
                ).fetchall()

                find = True

        elif 'modify-user' in request.form:
            # action of modify button
            id = request.form['modify-user']
            session['modify_user'] = id # store the user id to modify in session.
            return redirect(url_for("modifyUser.modifyUser"))

        elif 'aprove' in request.form:
            # action of aprove button
            id = request.form['aprove']
            session['aprove_user'] = id
            return redirect(url_for("aproveUser.aproveUser"))
            
        elif 'reject' in request.form:
            # action of reject button
            id = request.form['reject']

            utilities.loggerQuery(db, g.user['username'], 'rejectUser', id)
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()

        elif 'enable-proyect' in request.form:
            proyId = request.form['enable-proyect']
            db.execute(
                'UPDATE proyect SET status = ? WHERE id = ?',
                (1, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'enableProyect', proyId)
            db.commit()

        elif 'close-proyect' in request.form:
            proyId = request.form['close-proyect']
            db.execute(
                'UPDATE proyect SET status = ? WHERE id = ?',
                (0, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'closeProyect', proyId)
            db.commit()

        elif 'find-proyect' in request.form:
            proy = request.form['find-proyect']
            
            proyectsAll = db.execute(
                'SELECT * FROM proyect'
            ).fetchall()

            proyects = proyectsAll

            if proy != "":
                proyects = db.execute(
                    'SELECT * FROM proyect WHERE description = ?',
                    (proy,)
                ).fetchall()

            return render_template('index/root/rootUser.html', users=utilities.dataForUserTable(users, proyectsAll), areProyects = proyectsAll != [], proyects = utilities.dataForProyectTable(proyects))

        elif 'modify-proyect' in request.form:
            session['modify_proyect'] = request.form['modify-proyect']
            return redirect(url_for('modifyProyect.modifyProyect'))

        elif 'logs' in request.form:
            return redirect(url_for('logger.logger_index'))
 
    return render_template('index/root/rootUser.html', users=users, areProyects=proyects != [], proyects=proyects)


@bp.route('/manager', methods=('POST', 'GET'))
@manager_required
def manager():
    db = get_db()

    if request.method == 'POST':
        if 'modify' in request.form:
            session['modify_proyect'] = request.form['modify']
            return redirect(url_for('modifyProyect.modifyProyect'))

        elif 'enable-proyect' in request.form:
            proyId = request.form['enable-proyect']
            db.execute(
                'UPDATE proyect SET status = ? WHERE id = ?',
                (1, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'enableProyect', proyId)
            db.commit()

        elif 'close-proyect' in request.form:
            proyId = request.form['close-proyect']
            db.execute(
                'UPDATE proyect SET status = ? WHERE id = ?',
                (0, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'closeProyect', proyId)
            db.commit()

        elif 'create-proyect' in request.form:
            return redirect(url_for('createProyect.createProyect'))
            
        elif 'find-proyect' in request.form:
            proy = request.form['find-proyect'] # proyect to find

            if proy != "":

                proyects = db.execute(
                    'SELECT * FROM proyect WHERE description = ?',
                    (proy,)
                )
                return render_template('index/manager/managerUser.html', proyects = utilities.dataForProyectTable(proyects))

        elif 'logs' in request.form:
            return redirect(url_for('logger.logger_index'))

    proyects = db.execute(
        'SELECT * FROM proyect'
    ).fetchall()

    return render_template('index/manager/managerUser.html', proyects = utilities.dataForProyectTable(proyects))

@bp.route('/profile', methods=('POST', 'GET'))
@login_required
def profile():
    db = get_db()
    
    userInfo = db.execute(
        'SELECT firstname,secondname,role FROM user where username = ?',(g.user['username'],)
    ).fetchall()

    if request.method == 'POST':
        if 'change-password' in request.form:
            # action of crete a new user button
            return redirect(url_for("user.changePassword"))

    return render_template('index/user/user.html', userInfo = utilities.dataForUserProfileInfoTable(userInfo))


@bp.route('/profile/changePassword', methods=('POST', 'GET'))
@login_required
def changePassword():
    db = get_db()
    
    userPassword = db.execute(
        'SELECT password FROM user where username = ?',(g.user['username'],)
    ).fetchone()
    if request.method == 'POST':
        currentPassword = request.form['current-password']
        newPassword = request.form['new-password']
        
        error = None

        if not currentPassword:
            error = 'Current password required.'
        elif not newPassword:
            error = 'New password is required.'

        if error is None:
            try:
                # insert a new user to the user table in the database
                if check_password_hash(userPassword['password'], currentPassword):
                    db.execute(
                        "UPDATE user SET password = ? where username = ?",
                        (generate_password_hash(newPassword),g.user['username'])
                    )
                    utilities.loggerQuery(db, g.user['username'], 'changePassword', g.user['username'])
                    db.commit()

            except db.IntegrityError:
                error = f"Password cannot be changed."

            else:
                # the user changed it's password, redirect to login view
                return redirect(url_for("user.profile"))

        flash(error) # show any error that happened


    return render_template('index/user/changePassword.html')