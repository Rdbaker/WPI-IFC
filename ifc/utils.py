# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from functools import wraps

from flask import flash, request
from flask_login import current_user
from werkzeug.exceptions import Forbidden, Unauthorized


def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error),
                  category)


def permission_required(permission_name, apply_req_args=False,
                        fail_msg='You do not have permission to do that',
                        fail_exc=Forbidden):
    """Ensures that a user has the correct permission to access the view.

    This is used in a variety of ways to ensure proper permission gating on
    users. It will check if the current_user _has_ the attribute of the
    permission, then it will check to ensure that is a truthy value. If the user
    does not have the attribute, it will default to False.

    :param permission_name: string -- the string that corresponds to a
        permission to check on the user
    :param apply_req_args: bool -- sometimes the permission is a function
        that needs to be evaluated. If that is the case, pass True here and
        (via **kwargs expansion) the result of the request.view_args will be
        passed to the callable. Make sure your permission function aligns with
        the view_args names
    :param fail_msg: string (default: 'You do not have permission to do that')
        -- the message that will be passed to the exception class if the user
        does not have the permission
    :param fail_exc: class (default: werkzeug.exceptions.Forbidden) -- the class
        that should be `raise`d if the user does not have the permission. Please
        ensure that this both inherits from Exception AND is caught by either a
        blueprint or the app.

    example usage:
        >>> from ifc.utils import permission_required
        >>> @permission_required('can_view_party_by_id', True,
        ...                      fail_msg='You cannot view that party.')
        >>> def my_view_func():
        ...     return 'You can access this view', 200
    """
    def decorated_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            unauthenticated = not hasattr(current_user, permission_name)
            if unauthenticated:
                raise Unauthorized()
            allowed = getattr(current_user, permission_name, False)
            if apply_req_args and callable(allowed):
                allowed = allowed(**request.view_args)
            if not allowed:
                raise fail_exc(fail_msg)
            return f(*args, **kwargs)
        return wrapper
    return decorated_func


class InvalidAPIUsage(Exception):
    def __init__(self, message=None, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        result = dict(self.payload or ())
        result['message'] = self.message
        return result
