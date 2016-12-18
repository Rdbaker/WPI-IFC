# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import os

from flask import Flask, render_template, jsonify
from flask_admin import Admin
from flask_sslify import SSLify

import ifc.models as models
from ifc import public, user, party, ingest
from ifc.assets import assets
from ifc.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, \
    login_manager, migrate
from ifc.settings import ProdConfig
from ifc.utils import InvalidAPIUsage


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_admin(register_extensions(app))
    register_blueprints(app)
    register_errorhandlers(app)
    register_template_contexts(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""

    # only use SSL if we're on heroku
    if 'DYNO' in os.environ:
        SSLify(app)

    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    admin = Admin(app, name='IFC Event List - Admin Console',
                  template_mode='bootstrap3')
    csrf_protect.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return admin


def register_blueprints(app):
    """Register Flask blueprints."""
    app.register_blueprint(public.views.blueprint)
    app.register_blueprint(user.views.blueprint)
    app.register_blueprint(party.views.blueprint)
    app.register_blueprint(ingest.views.blueprint)
    return None


def register_errorhandlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)

    @app.errorhandler(InvalidAPIUsage)
    def handle_invalid_usage(error):
        """A handler for any endpoint that raises an InvalidUsage exception"""
        return jsonify(error.to_dict()), error.status_code

    return None


def register_admin(admin):
    """Set up the admin console for the app."""
    admin.add_view(models.UserModelView(models.User, db.session))
    admin.add_view(models.FraternityModelView(models.Fraternity, db.session))
    admin.add_view(models.PartyModelView(models.Party, db.session))
    admin.add_view(models.PreuserModelView(models.Preuser, db.session))
    admin.add_view(models.RoleModelView(models.Role, db.session))
    admin.index_view.is_accessible = models.AdminModelView._is_accessible
    admin.index_view.inaccessible_callback = \
        models.AdminModelView._inaccessible_callback


def register_template_contexts(app):
    """Adds the context processors we want in the Jinja templates."""
    @app.context_processor
    def inject_frats():
        return dict(fraternities=models.Fraternity.query.all())
