# -*- coding: utf-8 -*-
"""Ingets views."""
import csv
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug import secure_filename
from werkzeug.exceptions import Forbidden

import ifc.models as m

blueprint = Blueprint('ingest', __name__, url_prefix='/ingest', static_folder='../static')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1] in ['csv']


@blueprint.route('/', methods=['GET', 'POST'])
#@login_required
def upload_file():
    #if current_user.is_site_admin:
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            fpath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            file.save(fpath)
            ingest_file(fpath)
            flash('All data successfully ingested!', 'success')
            return redirect(url_for('public.home'))
    return render_template('ingest/index.html')
    #else:
    #    raise Forbidden()


def ingest_file(file_name):
    with open(file_name, 'r') as infile:
        # delete all pre-registration user models
        m.Preuser.query.delete()

        # create all pre-registration user models
        inread = csv.DictReader(infile)
        for brother in inread:
            # we only want WPI emails
            if '@wpi.edu' not in brother['email']:
                continue
            # strip '@wpi.edu' from the email, we just want the username
            brother['username'] = brother['email'][:brother['email'].index('@')].lower()
            brother.pop('email')
            # lol somebody's name was too long so I'm doing this
            brother['first_name'] = brother['first_name'].split()[0][:30]
            brother['chapter_admin'] = brother.get('chapter_admin', None) == 'True'
            brother['ifc_admin'] = brother.get('ifc_admin', None) == 'True'
            # placeholder logic to test, normally these are columns
            if brother['username'] in ['rdbaker', 'frlee']:
                brother['chapter_admin'] = True
                brother['ifc_admin'] = True
            m.Preuser.create(**brother)

        # delete users with no pre-registration user model
        for user in m.User.query.all():
            preuser = m.Preuser.query.filter( m.Preuser.username == user.username).first()
            if preuser is None:
                user.delete()
