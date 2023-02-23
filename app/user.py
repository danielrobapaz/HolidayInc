from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)
from app.auth import root_required, manager_required
from app.db import get_db
from . import utilities


# create the blueprint for the 'user'
bp = Blueprint('user', __name__)


@bp.route('/root', methods=('POST', 'GET'))
@root_required
def root():
    db = get_db()
    
    if request.method == 'POST':
        if 'create' in request.form:
            # action of crete a new user button
            return redirect(url_for("createUser.createUser"))

        elif 'proyect' in request.form:
            return redirect(url_for('createProyect.createProyect'))

        elif 'find-user' in request.form:
            user = request.form['find']

            if user != "":
                users = db.execute (
                    'SELECT id, username, firstname, secondname, role, auth FROM user WHERE role != ? AND username = ?',
                    ('admin', user)
                ).fetchall()

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
                    'SELECT * FROM proyect WHERE id = ?',
                    (proy,)
                ).fetchall()

            return render_template('index/root/rootUser.html', users=utilities.dataForUserTable(users, proyectsAll), areProyects = proyectsAll != [], proyects = utilities.dataForProyectTable(proyects))

        elif 'modify-proyect' in request.form:
            session['modify_proyect'] = request.form['modify-proyect']
            return redirect(url_for('modifyProyect.modifyProyect'))

        elif 'logs' in request.form:
            return redirect(url_for('logger.logger_index'))

    proyectsAll = db.execute(
        'SELECT * FROM proyect',
    ).fetchall()

    users = db.execute(
        'SELECT id, username, firstname, secondname, role, proyId, auth FROM user WHERE role != ?',
        ('admin',)
    ).fetchall()

    return render_template('index/root/rootUser.html', users=utilities.dataForUserTable(users, proyectsAll), areProyects = proyectsAll != [], proyects = utilities.dataForProyectTable(proyectsAll))


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
