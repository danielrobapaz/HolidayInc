import functools

# session is a dictionary that stores data acriss requests.
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

# creates a blueprint named 'auth'. A blueprint is a way
# to organize a group of related views.
bp = Blueprint('auth', __name__, url_prefix='/auth')


# /auth/register
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == "POST":
        # request for the input 
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                # insert a new user to the user table in the database
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password))
                )
                db.commit()

            except db.IntegrityError:
                error = f"User {username} is already registered."

            else:
                # the user was registered, redirect to login view
                return redirect(url_for("auth.login"))

        flash(error) # show any error that happened

    return render_template('auth/register.html')
        

# /auth/login
@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()
        error = None

        user = db.execute(
            "SELECT * FROM user WHERE username = ?", 
            (username,)
        ).fetchone()

        if user is None:
            error = 'User doesn\'t exist.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# a function that runds before the view function,
# no matter what URL is requested.
# It checks if a user id is stored in session
# and gets the user's data from the database 
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None

    else:
        g.user = get_db().execute(
            "SELECT * FROM user WHERE id = ?",
            (user_id)
        ).fetchone()


@bp.route('/logout')
def logout():
    # to logout wi need to remove the user id from
    # the session.
    session.clear()
    return redirect(url_for('index'))