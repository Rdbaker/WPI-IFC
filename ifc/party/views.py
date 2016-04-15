# -*- coding: utf-8 -*-
"""User views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.exceptions import Forbidden

from . import forms
from .models import Party
from ifc.utils import flash_errors

blueprint = Blueprint('party', __name__, url_prefix='/parties', static_folder='../static')


@blueprint.route('/')
@login_required
def parties():
    """List the parties."""
    return render_template('party/list.html', parties=current_user.fraternity.parties)


@blueprint.route('/new', methods=['GET'])
@login_required
def newparty():
    """Form to create a new party."""
    if current_user.can_create_party:
        return render_template('party/new.html', form=forms.NewPartyForm(user=current_user))
    else:
        raise Forbidden()

@blueprint.route('/new', methods=['POST'])
@login_required
def createparty():
    if current_user.can_create_party:
        form = forms.NewPartyForm(request.form)
        if form.validate_on_submit():
            party = Party.create(
                name=form.name.data,
                date=form.date.data,
                fraternity=current_user.fraternity,
                creator=current_user)
            flash('Party created.', 'success')
            return redirect(url_for('party.parties'))
        else:
            flash_errors(form)
            return render_template('party/new.html', form=form)
    else:
        raise Forbidden()
