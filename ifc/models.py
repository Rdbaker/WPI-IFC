# -*- coding: utf-8 -*-
"""The module containing all models in the app."""
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user
from werkzeug.exceptions import NotFound

from ifc.school.models import School  # noqa
from ifc.admin.models import Preuser  # noqa
from ifc.user.models import Role, User  # noqa
from ifc.party.models import Fraternity, Party, Guest  # noqa
from ifc.manage.models import Capacity  # noqa


class AdminModelView(ModelView):

    @property
    def simple_list_pager(self):
        return not current_user.is_admin

    @staticmethod
    def _is_accessible():
        return hasattr(current_user, 'is_site_admin') and \
            current_user.is_site_admin

    @staticmethod
    def _inaccessible_callback(*args):
        """Let's pretend this page doesn't exist."""
        raise NotFound()

    def is_accessible(self):
        """Blocks users that aren't allowed in."""
        return self._is_accessible()

    def inaccessible_callback(self, name, **kwargs):
        """Throws the user to a 401 page if they shouldn't be here."""
        return self._inaccessible_callback()

    def get_school_id(self):
        """Return the school ID of the current user."""
        return current_user.fraternity.school_id

    def get_query(self, bypass=False):
        """This method is an override from the base class. It should return a
        query that is filtered to only show the current user's school."""
        if hasattr(self, 'school_query'):
            return self.school_query
        else:
            return super(AdminModelView, self).get_query()


class SiteAdminModelView(AdminModelView):
    @staticmethod
    def _is_accessible():
        return hasattr(current_user, 'is_admin') and \
            current_user.is_admin


class UserModelView(AdminModelView):
    column_exclude_list = ['password', 'is_admin']
    column_searchable_list = ['email', 'first_name', 'last_name']
    form_excluded_columns = ['password', 'is_admin']

    @property
    def school_query(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return User.query
        else:
            return User.query.join(User.fraternity).join(Fraternity.school)\
                .filter_by(id=current_user.fraternity.school_id)


class RoleModelView(SiteAdminModelView):
    pass


class SchoolModelView(SiteAdminModelView):
    pass


class FraternityModelView(AdminModelView):
    form_excluded_columns = ['school']
    column_exclude_list = ['school']
    can_delete = False

    @property
    def school_query(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return Fraternity.query
        else:
            return Fraternity.query.join(Fraternity.school)\
                .filter_by(id=current_user.fraternity.school_id)


class PreuserModelView(AdminModelView):
    column_exclude_list = ['school_title']
    column_searchable_list = ['email', 'first_name', 'last_name']
    can_delete = False
    can_edit = False

    @property
    def school_query(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return Preuser.query
        else:
            return Preuser.query.filter_by(
                school_title=current_user.fraternity.school.title)


class PartyModelView(AdminModelView):
    column_searchable_list = ['name']
    can_edit = False

    @property
    def school_query(self):
        if hasattr(current_user, 'is_admin') and current_user.is_admin:
            return Party.query
        else:
            return Party.query.join(Party.fraternity).join(Fraternity.school)\
                .filter_by(id=current_user.fraternity.school_id)
