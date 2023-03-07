# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import modifyProyect_required
from app.db import get_db
from . import utilities

bp = Blueprint('proyectView', __name__, url_prefix='/root')

@bp.route('/proyects', methods=('POST', 'GET'))
@modifyProyect_required
def proyectView():
    db = get_db()

    if request.method == 'POST':
        if 'create-proyect' in request.form:
            return redirect(url_for('proyectView.createProyect'))
        
        elif 'enable-proyect' in request.form:
            proyId = request.form['enable-proyect']
            db.execute(
                'UPDATE proyect SET statusId = ? WHERE id = ?',
                (1, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'enableProyect', proyId)
            db.commit()

        elif 'close-proyect' in request.form:
            proyId = request.form['close-proyect']
            db.execute(
                'UPDATE proyect SET statusId = ? WHERE id = ?',
                (2, proyId)
            )
            utilities.loggerQuery(db, g.user['username'], 'closeProyect', proyId)
            db.commit()

        elif 'return' in request.form:
            return redirect(url_for('user.root'))

        elif 'find-proyect' in request.form:
            pass

        elif 'modify-proyect' in request.form:
            session['modify_proyect'] = request.form['modify-proyect']
            return redirect(url_for('modifyProyect.modifyProyect'))
    
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
    return render_template('proyect/proyectView.html', proyects=proyects)

@bp.route('/proyect/createProyect', methods=('GET', 'POST'))
@modifyProyect_required
def createProyect():
    if request.method == "POST":
        #request for the input
        description = request.form['description']
        start = request.form['starting-date']
        end = request.form['end-date']

        db = get_db()
        error = None

        if not description:
            error = 'A proyect name is required.'
        elif not utilities.isEndAfterStart(start, end):
            error = 'The proyect must end after it begins'

        if error is None:
            try:
                db.execute(
                    'INSERT INTO proyect (description, start, end, statusId) VALUES (?, ?, ?, ?)',
                    (description,start, end, 2)
                )
                utilities.loggerQuery(db, g.user['username'], 'createProyect', description)
                db.commit()

            except db.IntegrityError:
                error = f'Proyect is already created'

            else:
                return utilities.redirectFromProyect(g.user)

        flash(error)

    return render_template('proyect/createProyect.html')