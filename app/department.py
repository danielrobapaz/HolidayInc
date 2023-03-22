from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, flash
)
from app.auth import root_required, manager_required, login_required
from app.db import get_db
from . import utilities

bp = Blueprint('department', __name__, url_prefix='/deparment')

@bp.route('view', methods=('POST', 'GET'))
@root_required
def departmentView():
    db = get_db()
    if request.method == "POST":
        if 'return' in request.form:
            return redirect(url_for('user.root'))
        
        elif 'edit' in request.form:
            session['edit-dep'] = request.form['edit']
            return redirect(url_for('department.editDepartment'))

        elif 'delete' in request.form:
            delDep = request.form['delete']

            db.execute("DELETE FROM departments WHERE id = ?", (delDep))
            db.commit()

        elif 'create' in request.form:
            dep = request.form['dep']
            error = None

            if (len(dep) == 0):
                error = "Invalid department name"
            if error is None:
                try:
                    db.execute("INSERT INTO departments (description) values (?)", (dep,))
                    db.commit()

                except db.IntegrityError:
                    error = f'Department {dep} already exist'
        
            if not error is None:
                flash(error)

    departments = db.execute('SELECT * FROM departments').fetchall()
    return render_template('index/root/departmentsView.html', departments=departments)


@bp.route('edit', methods=("POST", "GET"))
@root_required
def editDepartment():
    db = get_db()
    id = session['edit-dep']
    if request.method == "POST":
        desc = request.form['desc']
        error = None

        if (len(desc) == 0):
            error = "Invalid name"
        if error is None:
            try:
                db.execute("UPDATE departments SET description = ? WHERE id = ?", (desc, id))
                db.commit()

            except db.IntegrityError:
                error = "Department already exist"
        
        if not error is None:
            flash(error)
        else:
            return redirect(url_for('department.departmentView'))

    dep = db.execute("SELECT * FROM departments WHERE id = ?", (id)).fetchone()
    return render_template('index/root/editDepartment.html', dep=dep)