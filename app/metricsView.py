# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from app.auth import root_required
from app.db import get_db
from . import utilities
import re

# creates a blueprint named 'createUser'. A blueprint is a way
# to organize a group of related views.
bp = Blueprint('metricsView', __name__, url_prefix='/metrics')

@bp.route('/metrics', methods=('POST', 'GET'))
@root_required
def metricsView():
    db = get_db()
    units = db.execute("SELECT * FROM metricsUnit").fetchall()

    if request.method == "POST":
        if "create" in request.form:
            dim = request.form['dim']
            metric = request.form['metric'].capitalize()
            error = None

            if not dim.isnumeric():
                error = 'Invalid dimension'
            if error is None:
                if all(unit['dimension'] != dim and unit['unit'] != metric for unit in units):

                    db.execute("INSERT INTO metricsUnit (dimension, unit) VALUES (?, ?)", (dim, metric,))
                    db.commit()

            else:
                flash(error)

        if "delete" in request.form:
            delId = request.form['delete']

            db.execute("DELETE FROM metricsUnit WHERE id = ?", (delId,))
            db.commit()

        if 'edit' in request.form:
            session['editId'] = request.form['edit']
            return redirect(url_for('metricsView.editMetric'))
        
        if 'return' in request.form:
            return redirect(url_for('user.root'))

    units = db.execute("SELECT * FROM metricsUnit").fetchall()

    return render_template('index/root/metricsView.html', units=units) 

@bp.route('/editMetric', methods=('POST', 'GET'))
@root_required
def editMetric():
    id = session['editId']
    db = get_db()

    if request.method == 'POST':
        dim = request.form['dim']
        unit = request.form['unit']

        db.execute("UPDATE metricsUnit SET dimension = ? WHERE id = ?", (dim, id,))
        db.execute("UPDATE metricsUnit SET unit = ? WHERE id = ?", (unit, id,))
        db.commit()

        return redirect(url_for('metricsView.metricsView'))
    unit = db.execute("SELECT dimension, unit FROM metricsUnit where id = ?", (id,)).fetchone()
    
    return render_template('index/root/editMetrics.html', unit=unit)