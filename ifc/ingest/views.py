# -*- coding: utf-8 -*-
"""Ingets views."""
import csv
import os

from flask import Blueprint, render_template, request, redirect, url_for,\
    flash, current_app
from flask_login import login_required, current_user
from werkzeug import secure_filename
from werkzeug.exceptions import Forbidden

from ifc import locales, models as m

blueprint = Blueprint('ingest', __name__, url_prefix='/ingest',
                      static_folder='../static')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ['csv']


@blueprint.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if hasattr(current_user, 'is_site_admin') and current_user.is_site_admin:
        if request.method == 'POST':
            file = request.files.get('file')
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                fpath = os.path.join(current_app.config['UPLOAD_FOLDER'],
                                     filename)
                file.save(fpath)
                ingest_file(fpath)
                flash(locales.Successes.DATA_INGESTED, 'success')
                return redirect(url_for('public.home'))
        return render_template('ingest/index.html')
    else:
        raise Forbidden()


def delete_school_preusers():
    """This function should ONLY be called where current_user is accessible.

    It will delete all preusers from the DB where their school title matches up
    with the current_user's school title.

    :return bool: False if some error was raised, else True
    """
    try:
        m.Preuser.query.filter_by(
            m.Preuser.school_title == current_user.fraternity.school.title)\
            .delete()
    except Exception:
        return False
    return True


def delete_relic_users():
    """This function should ONLY be called where current_user is accessible.

    It will delete all users from the DB where their school title matches up
    with the current_user's school title and they do not have a corresponding
    preuser

    :return bool: False if some error was raised, else True
    """
    try:
        school_users = m.User.query.join(m.User.fraternity)\
            .join(m.Fraternity.school).filter_by(
                id=current_user.fraternity.school_id).all()
        for user in school_users:
            preuser = m.Preuser.query.filter(
                m.Preuser.email == user.email,
                m.Preuser.school_title == current_user.fraternity.school.title)\
                    .first()
            if preuser is None:
                user.delete()
    except Exception:
        return False
    return True


def ingest_file(file_name):
    with open(file_name, 'r') as infile:
        # delete all pre-registration user models for the current_user's school
        delete_school_preusers()

        # create all pre-registration user models
        inread = csv.DictReader(infile)
        for brother in inread:
            # we only want WPI emails
            if '@wpi.edu' not in brother['email']:
                continue
            brother['email'] = brother.pop('email')
            # lol somebody's name was too long so I'm doing this
            brother['first_name'] = brother['first_name'].split()[0][:30]
            brother['chapter_admin'] = brother.get('chapter_admin',
                                                   None).lower() == 'true'
            brother['ifc_admin'] = brother.get('ifc_admin',
                                               None).lower() == 'true'
            m.Preuser.create(**brother)

        # delete users with no pre-registration user model
        delete_relic_users()
