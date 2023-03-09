from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from app.auth import root_required
from app.db import get_db
from . import utilities
import re

bp = Blueprint('clientView', __name__, url_prefix="/clients")

@bp.route('', methods=('POST', 'GET'))
def clientView():
    db = get_db()
    if request.method == "POST":
        if 'add' in request.form:
            return redirect(url_for('clientView.addClient'))
        
        if 'detail' in request.form:
            session['client_id'] = request.form['detail']
            return redirect(url_for('clientView.clientDetail'))
        
        if 'return' in request.form:
            return redirect(url_for('user.root'))
        
    clients = db.execute('SELECT * FROM clients').fetchall()

    return render_template('index/analist/analistView.html', clients=clients)

@bp.route('/addClient', methods=('POST', 'GET'))
def addClient():
    if request.method == 'POST':
        dni = request.form['dni']
        firstname = request.form['firstname']
        secondname = request.form['secondname']
        birthday = request.form['birthday']
        phone = request.form['phone']
        mail = request.form['mail']
        address = request.form['address']

        db = get_db()
        error = None

        if not re.search("^[\w\.]+@([\w-]+\.)+[\w-]{2,4}$", mail):
            error = 'You must enter a valid mail'

        if not re.search("^[V|E]-\d+$", dni):
            error = 'Invalid DNI'

        if not re.search("^\d{4}-\d{7}$", phone):
            error = 'Invalid phone number'

        if error is None:
            try:
                db.execute("""INSERT INTO clients
                                (dni, 
                                firstname,
                                secondname,
                                birthday,
                                tlf,
                                mail,
                                address)

                            VALUES
                                (?, ?, ?, ?, ?, ?, ?)""", 
                            (dni, firstname, secondname, birthday, phone, mail, address,))
                db.commit()

                return redirect(url_for('clientView.clientView'))
            
            except db.IntegrityError:
                error = 'Client already registered'
        flash(error)
    return render_template('index/analist/addClient.html')

@bp.route('/details', methods=('POST', 'GET'))
def clientDetail():
    db = get_db()

    if request.method == 'POST':
        if 'add' in request.form:
            return redirect(url_for('clientView.addCar'))
        
        if 'return' in request.form:
            return redirect(url_for('clientView.clientView'))

    clientId = session['client_id']
    cars = db.execute("SELECT * FROM cars WHERE ownerId = ?", (clientId)).fetchall()

    return render_template('index/analist/clientDetail.html', cars=cars)

@bp.route('/addCar', methods=('POST', 'GET'))
def addCar():
    if request.method == "POST":
        plaque = request.form['plaque']
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        bodywork = request.form['bodywork']
        motor = request.form['motor']
        color = request.form['color']
        problem = request.form['problem']

        db = get_db()
        error = None

#        if len(bodywork) != 17:
#            error = 'Invalid bodywork serial'
#
#        elif len(motor) != 17:
#            error = 'Invalid motor serial'
#
#        elif utilities.isYear(year):
#            error = 'Invalid year'

        if error is None:
            try:
                db.execute("""
                            INSERT INTO cars
                                (ownerId,
                                plaque,
                                brand,
                                model,
                                year,
                                bodyWorkSerial,
                                motorSerial,
                                color,
                                problem)
                                
                            VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?)""",
                            (session['client_id'], plaque, brand, model, year, bodywork, motor, color, problem,))

                db.commit()

                return redirect(url_for('clientView.clientDetail'))
            
            except db.IntegrityError:
                error = 'Car already registered'

        flash(error)
    return render_template('index/analist/addCar.html')