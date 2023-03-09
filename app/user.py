from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g, flash
)
from app.auth import root_required, manager_required, login_required
from app.db import get_db
from . import utilities
from werkzeug.security import generate_password_hash, check_password_hash


# create the blueprint for the 'user'
bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/root', methods=('POST', 'GET'))
@root_required
def root():
    if request.method == 'POST':
        if 'user' in request.form:
            return redirect(url_for('userView.userView'))

        elif 'proyect' in request.form:
            return redirect(url_for('proyectView.proyectView'))

        elif 'logs' in request.form:
            return redirect(url_for('logger.logger_index'))
        
        elif 'clients' in request.form:
            return redirect(url_for('clientView.clientView'))
        
    return render_template('index/root/rootUser.html')


@bp.route('/manager', methods=('POST', 'GET'))
@manager_required
def manager():
    return redirect(url_for('proyectView.proyectView'))

#@bp.route('/profile', methods=('POST', 'GET'))
#@login_required
#def profile():
#    db = get_db()
#    userInfo = db.execute(
#        """
#        SELECT 
#            u.firstname as firstname,
#            u.secondname as secondname,
#            r.name as role
#        FROM user u 
#        INNER JOIN roles r ON u.roleId = r.id 
#        WHERE username = ?""",
#        (g.user['username'],)
#    ).fetchall()
#
#    if request.method == 'POST':
#        if 'change-password' in request.form:
#            # action of crete a new user button
#            return redirect(url_for("user.changePassword"))
#
#    return render_template('index/user/user.html', userInfo = utilities.dataForUserProfileInfoTable(userInfo))
#
#
#@bp.route('/profile/changePassword', methods=('POST', 'GET'))
#@login_required
#def changePassword():
#    db = get_db()
#    
#    userPassword = db.execute(
#        'SELECT password FROM user where username = ?',(g.user['username'],)
#    ).fetchone()
#    if request.method == 'POST':
#        currentPassword = request.form['current-password']
#        newPassword = request.form['new-password']
#        
#        error = None
#
#        if not currentPassword:
#            error = 'Current password required.'
#        elif not newPassword:
#            error = 'New password is required.'
#
#        if error is None:
#            try:
#                # insert a new user to the user table in the database
#                if check_password_hash(userPassword['password'], currentPassword):
#                    db.execute(
#                        "UPDATE user SET password = ? where username = ?",
#                        (generate_password_hash(newPassword),g.user['username'])
#                    )
#                    utilities.loggerQuery(db, g.user['username'], 'changePassword', g.user['username'])
#                    db.commit()
#
#            except db.IntegrityError:
#                error = f"Password cannot be changed."
#
#            else:
#                # the user changed it's password, redirect to login view
#                return redirect(url_for("user.profile"))
#
#        flash(error) # show any error that happened
#
#    return render_template('index/user/changePassword.html')

