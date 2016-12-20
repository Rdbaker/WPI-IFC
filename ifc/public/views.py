# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import Blueprint, flash, redirect, render_template, request, \
    url_for, jsonify
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.exceptions import Forbidden

from ifc import locales, __version__
from ifc.extensions import login_manager
from ifc.public.forms import LoginForm
from ifc.user.forms import RegisterForm
from ifc.user.models import User
from ifc.party.models import Fraternity
from ifc.utils import flash_errors

blueprint = Blueprint('public', __name__, static_folder='../static')


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route('/', methods=['GET', 'POST'])
def home():
    """Home page."""
    form = LoginForm(request.form)
    # Handle logging in
    if request.method == 'POST':
        if form.validate_on_submit():
            login_user(form.user)
            flash(locales.Success.LOGIN_SUCCESS, 'success')
            redirect_url = request.args.get('next') or \
                url_for('parties.parties')
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template('public/home.html', form=form)


@blueprint.route('/logout/')
@login_required
def logout():
    """Logout."""
    logout_user()
    flash(locales.Success.LOGOUT_SUCCESS, 'info')
    return redirect(url_for('public.home'))


@blueprint.route('/register/', methods=['GET', 'POST'])
def register():
    """Register new user."""
    form = RegisterForm(request.form, csrf_enabled=False)
    if form.validate_on_submit():
        User.create(email=form.email.data, password=form.password.data,
                    active=True)
        flash(locales.Success.REGISTER_SUCCESS, 'success')
        return redirect(url_for('public.home'))
    else:
        flash_errors(form)
    return render_template('public/register.html', form=form)


@blueprint.route('/about/')
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template('public/about.html', form=form)


@blueprint.route('/status')
def status():
    """App status info."""
    return jsonify({
        'version': __version__
    })


@blueprint.route('/change-frat/<int:frat_id>')
@login_required
def change_fraternity(frat_id):
    """Change the user's fraternity, but only if they're an admin."""
    if not current_user.is_admin:
        raise Forbidden()
    frat = Fraternity.find_or_404(frat_id)
    current_user.update(fraternity=frat)
    redirect_url = request.referrer if request.referrer else \
        url_for('parties.parties')
    return redirect(redirect_url)
