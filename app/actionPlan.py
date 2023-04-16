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
    flag = False

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

        elif 'human' in request.form:
            return redirect(url_for('actionPlan.humanTalent'))
        
        elif 'supplie' in request.form:
            return redirect(url_for('actionPlan.supplie'))
        
        elif 'edit' in request.form:
            session['editAction'] = request.form['edit']
            return redirect(url_for('actionPlan.editAction'))

        elif 'search' in request.form:
            search = request.form['search']

            if search != '':
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
                                    WHERE proyectClientId = ? AND action = ?""", (proyId, search,)).fetchall()
                flag = True
    if not flag:
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
    
    total = 0
    for plan in plans:
        total = total + plan['total']

    return render_template('proyect/actionPlan.html', plans=plans, total=total)

@bp.route('create', methods=("POST", "GET"))
@modifyProyect_required
def createAction():
    currProy = session['currProy']
    proyId = session['actionProy']
    db = get_db()

    dates = db.execute("""
                        SELECT
                            start, end
                        FROM proyect
                        WHERE id = ?""", (currProy,)).fetchone()

    if request.method == "POST":
        action = request.form['action']
        activity = request.form['activity']
        start = request.form['starting-date']
        end = request.form['end-date']
        resp = request.form['resp']
        
        # human talent
        nWorkers = request.form['workers']
        costHour = request.form['costHour']

        # supplies
        category = ''
        if 'category' in request.form:
            category = request.form['category']
        supplie = request.form['supplie']
        metric = ''
        if 'metric' in request.form:
            metric = request.form['metric']
        quantity = request.form['quantity']
        costSupplie = request.form['costSupplie']

        error = None

        # verificamos la entrada
        startDate = datetime.strptime(start, "%Y-%m-%d").date()
        endDate = datetime.strptime(end, "%Y-%m-%d").date()

        days = (endDate-startDate).days + 1
        hours = days*8

        if days < 0:
            error='Invalid dates'

        if error is None:
            # verificamos que las fechas de inicio y fin ingresadas 
            if startDate < dates['start'] or startDate > dates['end']:
                error = "Invalid dates, out of proyect range"

            elif endDate < dates['start'] or endDate > dates['end']:
                error = "Invalid dates, out of proyect range"

            
        # verificamos human talent
        if error is None:
            if not nWorkers.isnumeric():
                error = "Invalid number of workers"

            elif not costHour.isnumeric():
                error = "Invalid cost per hour"

        if error is None:
            nWorkers = int(nWorkers)
            costHour = int(costHour)

            if nWorkers == 0:
                error = "Invalid number of workers"

            elif costHour == 0:
                error = "Invalid cost per hour"

        # verificamos suppli
        if error is None:
            if costSupplie != '' and not costSupplie.isnumeric():
                error = "Invalid cost of supplie"

            if quantity != '' and not quantity.isnumeric():
                error = "Invalid quantity of supplie"

        if error is None:
            # calculo del total de talento humano
            totalHumanTalent = hours*costHour

            # calculo del total de supplie
            totalSupplie = 0
            if not '' in [category, supplie, metric, costSupplie, quantity]:
               # find dimension of the supplie
               totalSupplie = int(quantity)*int(costHour)
            
            total = totalHumanTalent+totalSupplie

            try:
                db.execute("""
                            INSERT INTO actionPlan
                                (proyectClientId, action, activity,
                                 start, end, hours, 
                                 responsibleId, nWorkers, costPerHour,
                                 totalHumanTalent, category, supplieName,
                                 metricId, quantity, costSupplie, 
                                 totalSupplie, total)
                            VALUES
                                (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", 
                            (proyId, action, activity, 
                             start, end, hours, 
                             resp, nWorkers, costHour,
                             totalHumanTalent, category, supplie, 
                             metric, quantity, costSupplie, totalSupplie,
                             total,))

                db.commit()

                return redirect(url_for('actionPlan.actionPlanView'))

            except db.IntegrityError:
                error = "db error"

        flash(error)

    responsibles = db.execute("SELECT * FROM user WHERE roleId != 1 AND roleId != 2").fetchall()
    metrics = db.execute("SELECT * FROM metricsUnit").fetchall()

    return render_template('proyect/createAction.html', responsibles=responsibles, metrics=metrics)

@bp.route('edit', methods=("POST", "GET"))
@modifyProyect_required
def editAction():
    currProy = session['currProy']
    actionId = session['editAction']
    db = get_db()

    dates = db.execute("""
                        SELECT
                            start, end
                        FROM proyect
                        WHERE id = ?""", (currProy,)).fetchone()

    if request.method == "POST":
        action = request.form['action']
        activity = request.form['activity']
        start = request.form['starting-date']
        end = request.form['end-date']

        if 'resp' in request.form:
            resp = request.form['resp']
            db.execute("""
                        UPDATE actionPlan
                        SET responsibleId = ?
                        WHERE id =?""", (resp, actionId,))
            db.commit()
        
        # human talent
        nWorkers = request.form['workers']
        costHour = request.form['costHour']

        # supplies
        if 'category' in request.form:
            category = request.form['category']
            db.execute("""
                        UPDATE actionPlan
                        SET category = ?
                        WHERE id = ?""", (category, actionId,))

            db.commit()
        supplie = request.form['supplie']
        
        if 'metric' in request.form:
            metric = request.form['metric']
            db.execute("""
                        UPDATE actionPlan
                        SET metricId = ?
                        WHERE id = ?""", (metric, actionId,))
            db.commit()

        quantity = request.form['quantity']
        costSupplie = request.form['costSupplie']

        error = None

        # verificamos la entrada
        startDate = datetime.strptime(start, "%Y-%m-%d").date()
        endDate = datetime.strptime(end, "%Y-%m-%d").date()

        days = (endDate-startDate).days + 1
        hours = days*8

        if days < 0:
            error='Invalid dates'

        if error is None:
            # verificamos que las fechas de inicio y fin ingresadas 
            if startDate < dates['start'] or startDate > dates['end']:
                error = "Invalid dates, out of proyect range"

            elif endDate < dates['start'] or endDate > dates['end']:
                error = "Invalid dates, out of proyect range"

            
        # verificamos human talent
        if error is None:
            if not nWorkers.isnumeric():
                error = "Invalid number of workers"

            elif not costHour.isnumeric():
                error = "Invalid cost per hour"

        if error is None:
            nWorkers = int(nWorkers)
            costHour = int(costHour)

            if nWorkers == 0:
                error = "Invalid number of workers"

            elif costHour == 0:
                error = "Invalid cost per hour"

        # verificamos suppli
        if error is None:
            if costSupplie != '' and not costSupplie.isnumeric():
                error = "Invalid cost of supplie"

            if quantity != '' and not quantity.isnumeric():
                error = "Invalid quantity of supplie"

        if error is None:
            totalHumanTalent = costHour * hours

            # update rest of the db
            db.execute("""
                        UPDATE actionPlan
                        SET action = ?
                        WHERE id = ?""", (action, actionId,))

            db.execute("""
                        UPDATE actionPlan
                        SET activity = ?
                        WHERE id = ?""", (activity, actionId,))

            db.execute("""
                        UPDATE actionPlan
                        SET start = ?
                        WHERE id = ?""", (start, actionId,))

            db.execute("""
                        UPDATE actionPlan
                        SET end = ?
                        WHERE id = ?""", (end, actionId,))

            db.execute("""
                        UPDATE actionPlan
                        SET nWorkers = ?
                        WHERE id = ?""", (nWorkers, actionId,))
            
            db.execute("""
                        UPDATE actionPlan
                        SET costPerHour = ?
                        WHERE id = ?""", (costHour, actionId,))
        
            db.execute("""
                        UPDATE actionPlan
                        SET supplieName = ?
                        WHERE id = ?""", (supplie, actionId,))
            
            db.execute("""
                        UPDATE actionPlan
                        SET costSupplie = ?
                        WHERE id = ?""", (costSupplie, actionId,))
            
            db.execute("""
                        UPDATE actionPlan
                        SET hours = ?
                        WHERE id = ?""", (hours, actionId,))

            db.execute("""
                        UPDATE actionPlan
                        SET quantity = ?
                        WHERE id = ?""", (quantity, actionId,))
            
            db.execute("""
                        UPDATE actionPlan
                        SET totalHumanTalent = ?
                        WHERE id = ?""", (totalHumanTalent, actionId,))
            db.commit()

            # actualizacion de precios
            action = db.execute("SELECT * FROM actionPlan WHERE id = ?", (actionId,)).fetchone()

            totalSupplie = 0
            supplieValues = [action['quantity'], action['category'], action['supplieName'], action['metricId'], action['costSupplie']]
            if not '' in supplieValues:
                # no hay valor nulo en el registro
                quantity = action['quantity']
                costSupplie = action['costSupplie']
                
                totalSupplie = quantity*costSupplie

            total = totalSupplie + totalHumanTalent

            db.execute("""
                        UPDATE actionPlan
                        SET totalSupplie = ?
                        WHERE id = ?""", (totalSupplie, actionId,))
            
            db.execute("""
                        UPDATE actionPlan
                        SET total = ?
                        WHERE id = ?""", (total, actionId))
            
            db.commit()

            return redirect(url_for('actionPlan.actionPlanView'))

        flash(error)

    responsibles = db.execute("SELECT * FROM user WHERE roleId != 1 AND roleId != 2").fetchall()
    metrics = db.execute("SELECT * FROM metricsUnit").fetchall()
    action = db.execute("SELECT * FROM actionPlan WHERE id = ?", (actionId,)).fetchone()
    return render_template('proyect/editAction.html', responsibles=responsibles, metrics=metrics, action=action) 

@bp.route('humanTalent', methods=("POST", "GET"))
@modifyProyect_required
def humanTalent():
    db = get_db()
    proyId = session['actionProy']
    flag = False

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

        elif 'action' in request.form:
            return redirect(url_for('actionPlan.actionPlanView'))
        
        elif 'supplie' in request.form:
            return redirect(url_for('actionPlan.supplie'))

        elif 'edit' in request.form:
            session['editAction'] = request.form['edit']
            return redirect(url_for('actionPlan.editAction'))
        
        elif 'search' in request.form:
            search = request.form['search']

            if search != '':
                plans = db.execute("""
                        SELECT 
                            plan.id as id,
                            plan.action as action,
                            plan.activity as activity,
                            plan.hours as hours,
                            plan.nWorkers as nWorkers,
                            user.firstname as firstname,
                            user.secondname as secondname,
                            plan.totalHumanTalent as total
                        FROM actionPlan plan
                        INNER JOIN user ON plan.responsibleId = user.id
                        WHERE proyectClientId = ? AND action = ?""", (proyId,search)).fetchall()

                flag = True
    
    if not flag:
        plans = db.execute("""
                            SELECT 
                                plan.id as id,
                                plan.action as action,
                                plan.activity as activity,
                                plan.hours as hours,
                                plan.nWorkers as nWorkers,
                                user.firstname as firstname,
                                user.secondname as secondname,
                                plan.totalHumanTalent as total
                            FROM actionPlan plan
                            INNER JOIN user ON plan.responsibleId = user.id
                        WHERE proyectClientId = ?""", (proyId,)).fetchall()
    
    total = 0
    for plan in plans:
        total = total + plan['total']

    return render_template('proyect/humanTalent.html', plans=plans, total=total)

@bp.route('supplie', methods=("POST", "GET"))
@modifyProyect_required
def supplie():
    db = get_db()
    proyId = session['actionProy']
    flag = False

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

        elif 'action' in request.form:
            return redirect(url_for('actionPlan.actionPlanView'))
        
        elif 'human' in request.form:
            return redirect(url_for('actionPlan.humanTalent'))
        
        elif 'edit' in request.form:
            session['editAction'] = request.form['edit']
            return redirect(url_for('actionPlan.editAction'))
        
        elif 'search' in request.form:
            search = request.form['search']

            if search != '':
                plans = db.execute("""
                        SELECT 
                            plan.id as id,
                            plan.action as action,
                            plan.activity as activity,
                            plan.category as category,
                            plan.supplieName as supplieName,
                            plan.quantity as quantity,
                            metrics.dimension as dimension,
                            metrics.unit as unit,
                            user.firstname as firstname,
                            user.secondname as secondname,
                            plan.totalSupplie as total
                        FROM actionPlan plan
                        INNER JOIN user ON plan.responsibleId = user.id
                        INNER JOIN metricsUnit metrics ON plan.metricId = metrics.id
                        WHERE proyectClientId = ? AND plan.totalSupplie != 0 and action == ?""", (proyId, search,)).fetchall()
                
                flag = True

    if not flag:            
        plans = db.execute("""
                            SELECT 
                                plan.id as id,
                                plan.action as action,
                                plan.activity as activity,
                                plan.category as category,
                                plan.supplieName as supplieName,
                                plan.quantity as quantity,
                                metrics.dimension as dimension,
                                metrics.unit as unit,
                                user.firstname as firstname,
                                user.secondname as secondname,
                                plan.totalSupplie as total
                            FROM actionPlan plan
                            INNER JOIN user ON plan.responsibleId = user.id
                            INNER JOIN metricsUnit metrics ON plan.metricId = metrics.id
                            WHERE proyectClientId = ? AND plan.totalSupplie != 0""", (proyId,)).fetchall()
    
    total = 0
    for plan in plans:
        total = total + plan['total']
    return render_template('proyect/supplie.html', plans=plans, total=total)