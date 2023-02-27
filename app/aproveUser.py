from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from app.auth import root_required
from app.db import get_db
from . import utilities

bp = Blueprint('aproveUser', __name__)

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
