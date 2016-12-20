# -*- coding: utf-8 -*-
"""Model unit tests."""
import flask
import pytest
from werkzeug.exceptions import NotFound

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
        assert bool(user.email)
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

    def test_can_delete_party_by_id_404(self, admin, president, user,
                                        other_user, other_pres):
        """Tests the can_delete_party_by_id method where a party doesn't
        exist."""
        for user_model in [admin, president, user, other_user, other_pres]:
            with pytest.raises(NotFound):
                user_model.can_delete_party_by_id(1)

    def test_can_view_party_by_id_404(self, admin, president, user,
                                      other_user, other_pres):
        """Tests the can_view_party_by_id method where a party doesn't
        exist."""
        for user_model in [admin, president, user, other_user, other_pres]:
            with pytest.raises(NotFound):
                user_model.can_view_party_by_id(1)

    def test_can_edit_guest_by_id_404(self, admin, president, user,
                                      other_user, other_pres):
        """Tests the can_edit_guest_by_id method where a guest doesn't
        exist."""
        for user_model in [admin, president, user, other_user, other_pres]:
            with pytest.raises(NotFound):
                user_model.can_edit_guest_by_id(1)

    def test_can_delete_party_by_id(self, admin, president, user, other_user,
                                    other_pres, party):
        """Tests the can_delete_party_by_id method."""
        party.save()
        assert admin.can_delete_party_by_id(party.id)
        assert president.can_delete_party_by_id(party.id)
        assert not user.can_delete_party_by_id(party.id)
        assert not other_user.can_delete_party_by_id(party.id)
        assert not other_pres.can_delete_party_by_id(party.id)

    def test_can_delete_party_by_id_assigns_global_party(self, admin, party):
        """Tests that the can_delete_party_by_id method assigns the found party
        to flask.g.party."""
        party.save()
        admin.can_delete_party_by_id(party.id)
        assert 'party' in flask.g
        assert flask.g.party is party

    def test_can_view_party_by_id(self, admin, president, user, other_user,
                                  other_pres, party):
        """Tests the can_view_party_by_id method."""
        party.save()
        assert admin.can_view_party_by_id(party.id)
        assert president.can_view_party_by_id(party.id)
        assert user.can_view_party_by_id(party.id)
        assert not other_user.can_view_party_by_id(party.id)
        assert not other_pres.can_view_party_by_id(party.id)

    def test_can_view_party_by_id_assigns_global_party(self, admin, party):
        """Tests that the can_view_party_by_id method assigns the found party
        to flask.g.party."""
        party.save()
        admin.can_view_party_by_id(party.id)
        assert 'party' in flask.g
        assert flask.g.party is party

    def test_can_edit_guest_by_id(self, admin, president, user, other_user,
                                  other_pres, guest):
        """Tests the can_edit_guest_by_id method."""
        guest.save()
        assert not admin.can_edit_guest_by_id(guest.id)
        assert not president.can_edit_guest_by_id(guest.id)
        assert user.can_edit_guest_by_id(guest.id)
        assert not other_user.can_edit_guest_by_id(guest.id)
        assert not other_pres.can_edit_guest_by_id(guest.id)

    def test_can_edit_guest_by_id_assigns_global_guest(self, admin, guest):
        """Tests that the can_edit_guest_by_id method assigns the found guest
        to flask.g.guest."""
        guest.save()
        admin.can_edit_guest_by_id(guest.id)
        assert 'guest' in flask.g
        assert flask.g.guest is guest

    def test_can_edit_guest_by_id_assigns_guest_and_party(self, admin, guest,
                                                          party):
        """Tests that the can_edit_guest_by_id method assigns the found guest
        and party to the flask.g object."""
        guest.save()
        party.save()
        admin.can_edit_guest_by_id(guest.id, party.id)
        assert 'guest' in flask.g
        assert flask.g.guest is guest
        assert 'party' in flask.g
        assert flask.g.party is party

    def test_can_edit_guest(self, admin, user, other_user, president,
                            other_pres, guest):
        """Tests the can_edit_guest method."""
        assert not admin.can_edit_guest(guest)
        assert not president.can_edit_guest(guest)
        assert user.can_edit_guest(guest)
        assert not other_user.can_edit_guest(guest)
        assert not other_pres.can_edit_guest(guest)
