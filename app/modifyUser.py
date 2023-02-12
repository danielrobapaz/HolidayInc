from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import generate_password_hash

from app.auth import root_required
from app.db import get_db


# creates a blueprint naned 'modifyUser'.
bp = Blueprint('modifyUser', __name__)

@bp.route('/modifyUser', methods=('GET', 'POST'))
@root_required
def modifyUser():
    return render_template('index/modifyUser.html')