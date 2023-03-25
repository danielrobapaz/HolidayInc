# session is a dictionary that stores data across requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from app.auth import modifyProyect_required
from app.db import get_db
from . import utilities
import re

bp = Blueprint('proyectView', __name__, url_prefix='/root')

@bp.route('/proyects', methods=('POST', 'GET'))
@modifyProyect_required
def proyectView():
    db = get_db()
    flag = False
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
            find = request.form['find-proyect']
            proyectsToFilter = db.execute(

                """SELECT
                 p.id as id,
                 p.description as description,
                 p.start as start,
                 p.end as end,
                 s.name as status
                FROM proyect p
                INNER JOIN proyectStatus s ON p.statusId = s.id"""        
            ).fetchall()

            proyectsFiltered = []
            for proyect in proyectsToFilter:
                if re.search(find, proyect['description']):
                    proyectsFiltered.append({
                        'id': proyect['id'],
                        'description': proyect['description'],
                        'start': proyect['start'],
                        'end': proyect['end'],
                        'status': proyect['status']
                    })

            proyects = proyectsFiltered
            flag = True

        elif 'modify-proyect' in request.form:
            session['modify_proyect'] = request.form['modify-proyect']
            return redirect(url_for('modifyProyect.modifyProyect'))
        
        elif 'logs' in request.form:
            return redirect(url_for('logger.logger_index'))
        
        elif 'detail' in request.form:
            session['proyId'] = request.form['detail']
            return redirect(url_for('proyectView.detail'))
    
    if not flag:
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

@bp.route('/proyect/detail', methods=("POST", "GET"))
@modifyProyect_required
def detail():
    db = get_db()
    id = session['proyId']

    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('proyectView.proyectView'))
        
        elif 'add' in request.form:
            return redirect(url_for('proyectView.addClient'))

        elif 'delete' in request.form:
            id = request.form['delete']
            db.execute("""
                        DELETE FROM proyectClients
                        WHERE id = ?""", id)
            
            db.commit()
            
    currProy = db.execute("SELECT * from proyect WHERE id = ?", id).fetchone()

    proyectClients = db.execute("""
                                 SELECT
                                    pClients.id as id,
                                    cars.plaque as plaque,
                                    user.firstname as managerFirstName,
                                    user.secondname as managerSecondName,
                                    problems.problem as problem,
                                    pClients.subtotal as subtotal,
                                    pClients.observation as observation,
                                    pClients.solution as solution 
                                 FROM proyectClients as pClients
                                 INNER JOIN cars ON cars.id = pClients.carId
                                 INNER JOIN user ON user.id = pClients.managerId 
                                 INNER JOIN departments ON departments.id = pClients.departmentId
                                 INNER JOIN problems ON problems.id = pClients.problemId
                                 WHERE pClients.proyId = ?""", id).fetchall()

    return render_template('proyect/detail.html', proyectClients=proyectClients, currProy=currProy)


@bp.route('/addClient', methods=("POST", "GET"))
@modifyProyect_required
def addClient():
    db = get_db()
    proyId = session['proyId']

    if request.method == "POST":
        carId = request.form['plaque']
        managerId = request.form['manager']
        problemId = request.form['problem']
        solution = request.form['solution']
        total = request.form['total']
        observation = request.form['obser']

        # Buscamos el departamento correspondiente al problema
        
        depId = db.execute("SELECT depId FROM problems WHERE id = ?", problemId).fetchone()
        depId = depId['depId']

        # Buscamos el cliente al cual le pertenece el carro
        clientId = db.execute("SELECT ownerId FROM cars WHERE id =?", (carId)).fetchone()['ownerId']
        
        # agregamos registro a la base de datos
        db.execute("""
                    INSERT INTO proyectClients
                    (proyId, clientId, carId, managerId, 
                     departmentId, problemId, solution, subtotal,
                     observation)
                    VALUES
                        (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (proyId, clientId, carId, managerId, depId, problemId, solution,
                         total, observation,))
        
        db.commit()

        return redirect(url_for('proyectView.detail'))

    vehicules = db.execute("""SELECT 
                                cars.id as id,
                                cars.plaque as plaque, 
                                cars.brand as brand,
                                clients.firstname as firstname,
                                clients.secondname as secondname,
                                clients.dni as dni
                             FROM cars
                             INNER JOIN clients ON
                                cars.ownerId = clients.id""").fetchall()
    
    managers = db.execute("""SELECT 
                                id, 
                                firstname,
                                secondname
                                FROM user
                                WHERE roleId != 1 AND roleId != 2
                                """).fetchall()
    
    problems = db.execute("""SELECT 
                                problems.id as id,
                                problems.problem as problem,
                                departments.description as description
                                FROM problems
                                INNER JOIN departments ON
                                    problems.depId = departments.id""").fetchall()
    return render_template('proyect/addClient.html', vehicules=vehicules, managers=managers, problems=problems)