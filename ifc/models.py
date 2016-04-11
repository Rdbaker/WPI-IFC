# -*- coding: utf-8 -*-
"""The module containing all models in the app"""
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from ifc.user.models import Role, User
from ifc.party.models import Fraternity


class UserModelView(ModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['username']
    form_excluded_columns = ['password']

    def is_accessible(self):
        """Blocks users that aren't allowed in."""
        return current_user.is_site_admin

    def inaccessible_callback(self, name, **kwargs):
        """Throws the user to a 401 page if they shouldn't be here."""
        raise Unauthorized()

class RoleModelView(ModelView):
    can_delete = False
    can_edit = False

    def is_accessible(self):
        """Blocks users that aren't allowed in."""
        return current_user.is_site_admin

    def inaccessible_callback(self, name, **kwargs):
        """Throws the user to a 401 page if they shouldn't be here."""
        raise Unauthorized()
