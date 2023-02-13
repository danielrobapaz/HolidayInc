from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import generate_password_hash

from app.auth import root_required
from app.db import get_db


# creates a blueprint naned 'modifyUser'.
bp = Blueprint('modifyUser', __name__, url_prefix='/modifyUser')

@bp.route('/', methods=('GET', 'POST'))
@root_required
def modifyUser():
    # id of user to modify
    idModify = session['modify_user']
    db = get_db()
    
    if request.method == 'POST':
        if 'delete' in request.form:
            # delete the user from db
            db.execute(
                "DELETE FROM user WHERE id = ?",
                (idModify,)
            )
            db.commit()
            return redirect(url_for('user.index'))

        elif 'role' in request.form:
            return redirect(url_for('modifyUser.modify'))

    return render_template('index/modifyUser.html', id=session['modify_user'])


@bp.route('/modify', methods=('GET', 'POST'))
@root_required
def modify():
    if request.method == 'POST':
        error = None
        if len(request.form) == 0:
            error = 'Select a role.'

        else:
            roleModify = request.form['select']
            id = session['modify_user']
            db = get_db()

            db.execute(
                "UPDATE user SET role = ? WHERE id = ?",
                (roleModify, id)
            )
            db.commit()

            return redirect(url_for('user.index'))

        flash(error)
    return render_template('/index/modify.html')