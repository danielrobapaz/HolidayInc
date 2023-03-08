from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import generate_password_hash
from app.auth import root_required
from app.db import get_db
from . import utilities
import re

bp = Blueprint('analistView', __name__)

@bp.route('/analist', methods=('GET', 'POST'))
def analistView():
    # turbo query para clients
    return render_template('index/analist/analistView.html')