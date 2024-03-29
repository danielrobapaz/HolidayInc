from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for, g
)

from werkzeug.security import generate_password_hash
from . import utilities
from app.auth import root_required
from app.db import get_db


# creates a blueprint naned 'modifyUser'.
bp = Blueprint('modifyUser', __name__, url_prefix='/root/user')

@bp.route('/modifyUser', methods=('GET', 'POST'))
@root_required
def modifyUser():
    # id of user to modify
    idModify = session['modify_user']
    db = get_db()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            utilities.loggerQuery(db, g.user['username'], 'deleteUser', idModify)

            # delete the user from db
            db.execute("DELETE FROM user WHERE id = ?",(idModify,))
            db.execute("DELETE FROM proyectClients WHERE managerId = ?", (idModify,))
            db.execute("DELETE FROM actionPlan WHERE responsibleId = ?", (idModify,))
            db.commit()
            return redirect(url_for('userView.userView'))

        elif 'role' in request.form:
            return redirect(url_for('modifyUser.changeRole'))

        elif 'proyect' in request.form:
            return redirect(url_for('modifyUser.changeProyect'))

    return render_template('index/root/modifyUser.html', id=session['modify_user'])


@bp.route('/modifyUser/changeRole', methods=('GET', 'POST'))
@root_required
def changeRole():
    db = get_db()
    roles = db.execute("""SELECT 
                            id, name 
                          FROM roles
                          WHERE name != 'admin' and name != 'Waiting'""").fetchall()
    
    if request.method == 'POST':
        error = None

        if len(request.form) == 0:
            error = 'Select a role.'

        else:
            roleModify = request.form['select']
            id = session['modify_user']        
            db.execute(
                "UPDATE user SET roleId = ? WHERE id = ?",
                (roleModify, id)
            )
            
            username = utilities.findUsernameById(db, id)
            utilities.loggerQuery(db, g.user['username'], 'setRole', [username, roleModify])

            db.commit()

            return redirect(url_for('userView.userView'))

        flash(error)
    return render_template('/index/root/changeRole.html', roles = roles)

@bp.route('/modifyUser/changeProyect', methods=('GET', 'POST'))
@root_required
def changeProyect():
    db = get_db()
    proyects = db.execute(
        'SELECT * FROM proyect'
    )

    if request.method == 'POST':
        proyId = request.form['proyect']

        # update user table 
        db.execute(
            'UPDATE user SET proyId = ? WHERE id = ?',
            (proyId, session['modify_user']),
        )

        username = utilities.findUsernameById(db, session['modify_user'])
        utilities.loggerQuery(db, g.user['username'], 'setProyect', [username, proyId])

        db.commit()

        return redirect(url_for('user.root'))

    return render_template('/proyect/changeProyect.html', proyects = proyects)