# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, redirect, url_for, jsonify
from flask_login import login_required, current_user

blueprint = Blueprint('ifc-user', __name__, url_prefix='/users', static_folder='../static')


@blueprint.route('/')
@login_required
def members():
    """Redirect to parties list."""
    return redirect(url_for('party.parties'))


@blueprint.route('/me')
@login_required
def me():
    """Return the currently logged in user as a json object."""
    return jsonify(me=current_user.json_dict)
