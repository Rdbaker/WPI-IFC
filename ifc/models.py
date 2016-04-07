# -*- coding: utf-8 -*-
"""The module containing all models in the app"""
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from ifc.user.models import Role, User


class AdminModelView(ModelView):
    def is_accessible(self):
        """Blocks users that aren't allowed in."""
        return current_user.is_site_admin

    def inaccessible_callback(self, name, **kwargs):
        """Throws the user to a 401 page if they shouldn't be here."""
        raise Unauthorized()
