from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db


# create the blueprint for the 'user'
bp = Blueprint('user', __name__, url_prefix='/index')


@bp.route('/', methods=('POST', 'GET'))
@login_required
def index():
    if request.method == 'POST':
        pass

    db = get_db()
    users = db.execute(
        'SELECT id, username FROM user WHERE auth = 0'
    ).fetchall()
    
    return render_template('index/index.html', users=users)