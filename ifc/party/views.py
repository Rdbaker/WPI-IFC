# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('party', __name__, url_prefix='/parties', static_folder='../static')


@blueprint.route('/')
@login_required
def parties():
    """List the parties."""
    return render_template('users/members.html')
