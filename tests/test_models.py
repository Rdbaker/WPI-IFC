# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from ifc.user.models import User


@pytest.mark.usefixtures('db')
class TestUser:
    """User tests."""

    def test_get_by_id(self, user):
        """Get user by ID."""
        user.save()
        retrieved = User.find_by_id(user.id)
        assert retrieved == user

    def test_factory(self, db, user):
        """Test user factory."""
        assert bool(user.username)
        assert user.active is True
        assert user.check_password('myprecious')

    def test_check_password(self, preuser, role, frat):
        """Check password."""
        user = User.create(username=preuser.username,
                           password='foobarbaz123',
                           role_id=role.id, fraternity_id=frat.id)
        assert user.check_password('foobarbaz123') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self, user):
        """User full name."""
        assert user.full_name == user.first_name + ' ' + user.last_name
