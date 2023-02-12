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
            # se elimina el usuario de la bd
            return redirect(url_for('user.index'))

        elif 'role' in request.form:
            return redirect(url_for('modifyUser.modify'))

    return render_template('index/modifyUser.html', id=session['modify_user'])


@bp.route('/modify', methods=('GET', 'POST'))
@root_required
def modify():
    return render_template('/index/modify.html')