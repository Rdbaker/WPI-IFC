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
        assert user.check_password('example')

    def test_check_password(self, user):
        """Check password."""
        assert user.check_password('example') is True
        assert user.check_password('barfoobaz') is False

    def test_full_name(self, user):
        """User full name."""
        assert user.full_name == user.first_name + ' ' + user.last_name

    def test_is_site_admin(self, admin, president, user):
        """Tests the is_site_admin property."""
        assert admin.is_site_admin
        assert not president.is_site_admin
        assert not user.is_site_admin

    def test_is_chapter_admin(self, admin, president, user):
        """Tests the is_chapter_admin property."""
        assert not admin.is_chapter_admin
        assert president.is_chapter_admin
        assert not user.is_chapter_admin

    def test_can_delete_party(self, admin, president, user, party, other_user,
                              other_pres):
        """Tests the can_delete_party method."""
        assert admin.can_delete_party(party)
        assert president.can_delete_party(party)
        assert not user.can_delete_party(party)
        assert not other_user.can_delete_party(party)
        assert not other_pres.can_delete_party(party)

    def test_can_create_party(self, admin, president, user):
        """Tests the can_create_party property."""
        assert admin.can_create_party
        assert president.can_create_party
        assert not user.can_create_party

    def test_can_view_party(self, admin, president, other_pres, user,
                            other_user, party):
        """Tests the can_view_party method."""
        assert admin.can_view_party(party)
        assert president.can_view_party(party)
        assert user.can_view_party(party)
        assert not other_pres.can_view_party(party)
        assert not other_user.can_view_party(party)
