from flask import (
    Blueprint, redirect, render_template, request, session, url_for
)
from app.auth import root_required
from app.db import get_db
from . import utilities


# create the blueprint for the 'user'
bp = Blueprint('user', __name__)


@bp.route('/root', methods=('POST', 'GET'))
@root_required
def root():
    db = get_db()
    users = db.execute(
        'SELECT id, username, firstname, secondname, role, proyId, auth FROM user WHERE role != ?',
        ('admin',)
    ).fetchall()

    proyects = db.execute(
        'SELECT * FROM proyect',
    ).fetchall()


    if request.method == 'POST':
        if 'create' in request.form:
            # action of crete a new user button
            return redirect(url_for("createUser.createUser"))

        elif 'proyect' in request.form:
            return redirect(url_for('createProyect.createProyect'))

        elif 'find' in request.form:
            user = request.form['find']

            if user != "":
                users = db.execute (
                    'SELECT id, username, firstname, secondname, role, auth FROM user WHERE role != ? AND username = ?',
                    ('admin', user)
                ).fetchall()

        elif 'modify' in request.form:
            # action of modify button
            id = request.form['modify']
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
            db.execute(
                'DELETE FROM user WHERE id = ?',
                (id,)
            )
            db.commit()
    
    return render_template('index/root/rootUser.html', users=utilities.dataForUserTable(users, proyects), areProyects = proyects != [])