# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import modifyProyect_required
from app.db import get_db
from . import utilities

bp = Blueprint('createProyect', __name__)

@bp.route('/createProyect', methods=('GET', 'POST'))
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
                return utilities.redirectToUser(g.user)

        flash(error)

    return render_template('proyect/createProyect.html')