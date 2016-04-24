# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template
from flask_admin import Admin

import ifc.models as models
from ifc import public, user, party, ingest
from ifc.assets import assets
from ifc.extensions import bcrypt, cache, csrf_protect, db, debug_toolbar, login_manager, migrate
from ifc.settings import ProdConfig


def create_app(config_object=ProdConfig):
    """An application factory, as explained here: http://flask.pocoo.org/docs/patterns/appfactories/.

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_admin(register_extensions(app))
    register_blueprints(app)
    register_errorhandlers(app)
    return app


def register_extensions(app):
    """Register Flask extensions."""
    assets.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    admin = Admin(app, name='WPI IFC - Admin Console', template_mode='bootstrap3')
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
    return None


def register_admin(admin):
    """Set up the admin console for the app."""
    admin.add_view(models.UserModelView(models.User, db.session))
    admin.add_view(models.FraternityModelView(models.Fraternity, db.session))
    admin.add_view(models.PreuserModelView(models.Preuser, db.session))
    admin.add_view(models.RoleModelView(models.Role, db.session))
