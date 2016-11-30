# -*- coding: utf-8 -*-
"""The module containing all models in the app"""
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import Unauthorized

from ifc.admin.models import Preuser  # noqa
from ifc.user.models import Role, User  # noqa
from ifc.party.models import Fraternity, Party, Guest  # noqa


class AdminModelView(ModelView):
    def is_accessible(self):
        """Blocks users that aren't allowed in."""
        return hasattr(current_user, 'is_site_admin') and \
            current_user.is_site_admin

    def inaccessible_callback(self, name, **kwargs):
        """Throws the user to a 401 page if they shouldn't be here."""
        raise Unauthorized()


class UserModelView(AdminModelView):
    column_exclude_list = ['password']
    column_searchable_list = ['username', 'first_name', 'last_name']
    form_excluded_columns = ['password']


class RoleModelView(AdminModelView):
    can_delete = False
    can_edit = False


class FraternityModelView(AdminModelView):
    can_delete = False


class PreuserModelView(AdminModelView):
    column_searchable_list = ['username', 'first_name', 'last_name']
    can_delete = False
    can_edit = False


class PartyModelView(AdminModelView):
    column_searchable_list = ['name']
    can_edit = False
