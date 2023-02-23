from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)
from app.auth import login_required
from app.db import get_db
from . import utilities


# create the blueprint for the 'logger'
bp = Blueprint('logger', __name__)


@bp.route('/logger', methods=('POST', 'GET'))
@login_required
def logger_index():
    db = get_db()
    logs = db.execute(
        'SELECT * FROM logger'
    ).fetchall()

    return render_template('index/logger/loggerIndex.html', areLogs = logs != [], logs = utilities.dataForLoggerTable(logs))