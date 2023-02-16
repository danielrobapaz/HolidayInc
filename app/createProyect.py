# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import root_required
from app.db import get_db

bp = Blueprint('createProyect', __name__)

@bp.route('/createProyect', methods=('GET', 'POST'))
@root_required
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

        if error is None:
            try:
                db.execute(
                    'INSERT INTO proyect (description, start, end, status) VALUES (?, ?, ?, ?)',
                    (description,start, end, 0)
                )
                db.commit()

            except db.IntegrityError:
                error = f'Proyect is already created'

            else:
                return redirect(url_for('user.index'))

        flash(error)

    return render_template('index/createProyect.html')