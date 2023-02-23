from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)
from app.auth import root_required, manager_required
from app.db import get_db
from . import utilities


# create the blueprint for the 'logger'
bp = Blueprint('logger', __name__)


@bp.route('/logger', methods=('POST', 'GET'))
# @root_required
def logger_index():
    db = get_db()
    logs = db.execute(
        'SELECT * FROM logger'
    ).fetchall()

    if request.method == 'POST':
        if 'delete-log' in request.form:
            logId = request.form['delete-log']
            db.execute(
                'DELETE FROM logger where id = ?',
                (logId)
            )
            db.commit()
    #     if 'create' in request.form:
    #         # action of crete a new user button
    #         return redirect(url_for("createUser.createUser"))

    #     elif 'proyect' in request.form:
    #         return redirect(url_for('createProyect.createProyect'))

    #     elif 'find-user' in request.form:
    #         user = request.form['find']

    #         if user != "":
    #             users = db.execute (
    #                 'SELECT id, username, firstname, secondname, role, auth FROM user WHERE role != ? AND username = ?',
    #                 ('admin', user)
    #             ).fetchall()

    #     elif 'modify-user' in request.form:
    #         # action of modify button
    #         id = request.form['modify-user']
    #         session['modify_user'] = id # store the user id to modify in session.
    #         return redirect(url_for("modifyUser.modifyUser"))

    #     elif 'aprove' in request.form:
    #         # action of aprove button
    #         id = request.form['aprove']
    #         session['aprove_user'] = id
    #         return redirect(url_for("aproveUser.aproveUser"))
            
    #     elif 'reject' in request.form:
    #         # action of reject button
    #         id = request.form['reject']
    #         db.execute(
    #             'DELETE FROM user WHERE id = ?',
    #             (id,)
    #         )
    #         db.commit()

    #     elif 'enable-proyect' in request.form:
    #         proyId = request.form['enable-proyect']
    #         db.execute(
    #             'UPDATE proyect SET status = ? WHERE id = ?',
    #             (1, proyId)
    #         )
    #         db.commit()

    #     elif 'close-proyect' in request.form:
    #         proyId = request.form['close-proyect']
    #         db.execute(
    #             'UPDATE proyect SET status = ? WHERE id = ?',
    #             (0, proyId)
    #         )
    #         db.commit()

    #     elif 'find-proyect' in request.form:
    #         proy = request.form['find-proyect']
            
    #         proyectsAll = db.execute(
    #             'SELECT * FROM proyect'
    #         ).fetchall()

    #         proyects = proyectsAll

    #         if proy != "":
    #             proyects = db.execute(
    #                 'SELECT * FROM proyect WHERE id = ?',
    #                 (proy,)
    #             ).fetchall()

    #         return render_template('index/logger/loggerIndex.html', users=utilities.dataForUserTable(users, proyectsAll), areProyects = proyectsAll != [], proyects = utilities.dataForProyectTable(proyects))

    #     elif 'modify-proyect' in request.form:
    #         session['modify_proyect'] = request.form['modify-proyect']
    #         return redirect(url_for('modifyProyect.modifyProyect'))

    # proyectsAll = db.execute(
    #     'SELECT * FROM proyect',
    # ).fetchall()

    # return render_template('index/logger/loggerIndex.html', areLogs = logsAll != [], proyects = utilities.dataForProyectTable(proyectsAll))
    return render_template('index/logger/loggerIndex.html', areLogs = logs != [], logs = utilities.dataForLoggerTable(logs))

# @bp.route('/manager', methods=('POST', 'GET'))
# @manager_required
# def manager():
#     db = get_db()

#     if request.method == 'POST':
#         if 'modify' in request.form:
#             session['modify_proyect'] = request.form['modify']
#             return redirect(url_for('modifyProyect.modifyProyect'))

#         elif 'enable-proyect' in request.form:
#             proyId = request.form['enable-proyect']
#             db.execute(
#                 'UPDATE proyect SET status = ? WHERE id = ?',
#                 (1, proyId)
#             )
#             db.commit()

#         elif 'close-proyect' in request.form:
#             proyId = request.form['close-proyect']
#             db.execute(
#                 'UPDATE proyect SET status = ? WHERE id = ?',
#                 (0, proyId)
#             )
#             db.commit()

#         elif 'create-proyect' in request.form:
#             return redirect(url_for('createProyect.createProyect'))
            
#         elif 'find-proyect' in request.form:
#             proy = request.form['find-proyect'] # proyect to find

#             if proy != "":

#                 proyects = db.execute(
#                     'SELECT * FROM proyect WHERE description = ?',
#                     (proy,)
#                 )
#                 return render_template('index/manager/managerUser.html', proyects = utilities.dataForProyectTable(proyects))


#     proyects = db.execute(
#         'SELECT * FROM proyect'
#     ).fetchall()

#     return render_template('index/manager/managerUser.html', proyects = utilities.dataForProyectTable(proyects))