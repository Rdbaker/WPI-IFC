# -*- coding: utf-8 -*-
"""Admin views."""
from flask import Blueprint, render_template
from flask_login import login_required

blueprint = Blueprint('ifc-admin', __name__, url_prefix='/ifc-admin', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """Show the base template."""
    return render_template('admin/index.html')
