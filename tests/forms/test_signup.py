# -*- coding: utf-8 -*-
"""Test forms."""
from ifc.user.forms import RegisterForm


class TestRegisterForm:
    """Register form."""

    def test_validate_user_already_registered(self, user):
        """Enter email that is already registered."""
        form = RegisterForm(email=user.email,
                            password='example', confirm='example')

        assert form.validate() is False
        assert 'Email already registered' in form.email.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = RegisterForm(email='newemail@test.com',
                            password='example', confirm='example')
        assert form.validate() is True
