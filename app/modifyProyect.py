# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import modifyProyect_required
from app.db import get_db
from . import utilities

bp = Blueprint('modifyProyect', __name__)

@bp.route('/modifyProyect', methods=('GET', 'POST'))
@modifyProyect_required
def modifyProyect():
    if request.method == 'POST':
        if 'change-dates' in request.form:
            return redirect(url_for('modifyProyect.changeDates'))

        elif 'delete' in request.form:
            # delete the proyect in db
            db = get_db()
            idProy = session['modify_proyect']

            db.execute(
                'DELETE FROM proyect WHERE id = ?',
                (idProy)
            )

            # unauthorize every user wich proyect id is proyId
            db.execute(
                'UPDATE user set auth = 0 WHERE proyId = ?',
                (idProy)
            )
            
            # delete the proyId of every user
            db.execute(
                'UPDATE user SET proyId = NULL WHERE proyId = ?',
                (idProy)
            )
            db.commit()

            # return to the respective view
            return utilities.redirectToUser(g.user)

    return render_template('proyect/modifyProyect.html')

@bp.route('/changeDatesProyect', methods=('GET', 'POST'))
@modifyProyect_required
def changeDates():
    if request.method == 'POST':
        start = request.form['starting-date']
        end = request.form['end-date']

        error = None

        if not utilities.isEndAfterStart(start, end):
            error = 'The proyect must end after it begins'

        if error is None:
            # update de dates in the db
            db = get_db()
            idProy = session['modify_proyect']

            db.execute(
                'UPDATE proyect SET start = ? WHERE id = ?',
                (start, idProy)
            )

            db.execute(
                'UPDATE proyect SET end = ? WHERE id = ?',
                (end, idProy)
            )

            db.commit()

            return utilities.redirectToUser(g.user)

        flash(error)


    return render_template('proyect/changeDates.html')