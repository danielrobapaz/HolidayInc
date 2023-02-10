from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db


# create the blueprint for the 'user'
bp = Blueprint('user', __name__, url_prefix='/index')


@bp.route('/', methods=('POST', 'GET'))
@login_required
def index():
    db = get_db()

    if request.method == 'POST':
        if 'create' in request.form:
            pass
        elif 'aprove' in request.form:
            id = request.form['aprove']
            db.execute(
                'UPDATE user SET auth = 1 WHERE id = ?',
                (id,)
            )
            db.commit()
        elif 'reject' in request.form:
            id = request.form['reject']
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()

    
    db = get_db()
    users = db.execute(
        'SELECT id, username FROM user WHERE auth = 0'
    ).fetchall()
    
    return render_template('index/index.html', users=users)