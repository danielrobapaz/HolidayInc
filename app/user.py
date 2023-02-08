from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from app.auth import login_required
from app.db import get_db


# create the blueprint for the 'user'
bp = Blueprint('user', __name__)


@bp.route('/')
def index():
    return render_template('index/index.html')