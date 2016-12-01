# -*- coding: utf-8 -*-
"""Test forms."""
from ifc.user.forms import RegisterForm


class TestRegisterForm:
    """Register form."""

    def test_validate_user_already_registered(self, user):
        """Enter username that is already registered."""
        form = RegisterForm(username=user.username,
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Username already registered' in form.username.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = RegisterForm(username='newusername',
                            password='example', confirm='example')
        assert form.validate() is True
