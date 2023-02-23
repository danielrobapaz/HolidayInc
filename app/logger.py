from flask import (
    Blueprint, redirect, render_template, request, session, url_for, g
)
from app.auth import login_required
from app.db import get_db
from . import utilities
import re


# create the blueprint for the 'logger'
bp = Blueprint('logger', __name__)


@bp.route('/logger', methods=('POST', 'GET'))
@login_required
def logger_index():
    db = get_db()
        
    logs = db.execute(
        'SELECT * FROM logger'
    ).fetchall()


    if request.method == 'POST':
        if 'find-log' in request.form:
            find = request.form['find-log']

            logsFind = []
            if find != "":
                for log in logs:
                    if re.search(find, log['event']):
                        logsFind.append({
                          'id': log['id'],
                          'date': log['date'],
                          'event': log['event'],
                          'user': log['user']  
                        })

                return render_template('index/logger/loggerIndex.html', logs = logsFind) 

        elif 'return' in request.form:
            return utilities.redirectToUser(g.user)

    if g.user['role'] != 'admin':
        logs = db.execute(
            'SELECT * FROM logger WHERE user = ?',
            (g.user['username'],)
        ).fetchall()

    return render_template('index/logger/loggerIndex.html', logs = utilities.dataForLoggerTable(logs))