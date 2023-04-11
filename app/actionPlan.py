# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import modifyProyect_required
from app.db import get_db
from . import utilities
import re
from datetime import datetime

bp = Blueprint('actionPlan', __name__, url_prefix='/plan')

@bp.route('', methods=('POST', 'GET'))
@modifyProyect_required
def actionPlanView():
    proyId = session['actionProy']
    db = get_db()

    if request.method == "POST":
        if 'return' in request.form:
            session['proyId'] = proyId
            return redirect(url_for('proyectView.detail'))
        
        elif 'create' in request.form:
            return redirect(url_for('actionPlan.createAction'))
        
        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute("DELETE FROM actionPlan WHERE id = ?", (id,))
            db.commit()
    
    plans = db.execute("""
                        SELECT 
                            plan.id as id,
                            plan.action as action,
                            plan.activity as activity,
                            plan.start as start,
                            plan.end as end,
                            plan.hours as hours,
                            user.firstname as firstname,
                            user.secondname as secondname,
                            plan.total as total
                        FROM actionPlan plan
                        INNER JOIN user ON plan.responsibleId = user.id
                        WHERE proyectClientId = ?""", (proyId,)).fetchall()
    
    return render_template('proyect/actionPlan.html', plans=plans)

@bp.route('create', methods=("POST", "GET"))
@modifyProyect_required
def createAction():
    proyId = session['actionProy']
    db = get_db()

    if request.method == "POST":
        action = request.form['action']
        activity = request.form['activity']
        start = request.form['starting-date']
        end = request.form['end-date']
        resp = request.form['resp']

        error = None

        startDate = datetime.strptime(start, "%Y-%m-%d")
        endDate = datetime.strptime(end, "%Y-%m-%d")

        days = (endDate-startDate).days + 1
        hours = days*8

        if days < 0:
            error='Invalid dates'

        try:
            db.execute("""
                        INSERT INTO actionPlan
                        (proyectClientId, action, activity,
                         start, end, hours, responsibleId)
                        VALUES
                            (?, ?, ?, ?, ?, ?, ?)""", 
                        (proyId, action, activity, start, end, hours, resp,))

            db.commit()

            return redirect(url_for('actionPlan.actionPlanView'))
        
        except db.IntegrityError:
            error = "db error"

        flash(error)

    responsibles = db.execute("SELECT * FROM user WHERE roleId != 1 AND roleId != 2").fetchall()
    return render_template('proyect/createAction.html', responsibles=responsibles)