# -*- coding: utf-8 -*-
"""Model unit tests."""
from datetime import date

import pytest

from ifc.models import Party


@pytest.mark.usefixtures('db')
class TestParty:
    """Party tests."""
    def test_fraternity_user_alignment(self, other_frat, user):
        with pytest.raises(AssertionError):
            Party.create(name='my party', fraternity=other_frat, creator=user,
                         date=date.today())

    def test_guest_is_on_list(self, party, guest):
        """Test party.is_on_guest_list with somebody who is on the list."""
        assert party.is_on_guest_list(guest.name)

    def test_guest_not_on_list(self, party, other_guest):
        """Test party.is_on_guest_list with somebody who is not on the list."""
        assert not party.is_on_guest_list(other_guest.name)

    def test_male_guests(self, party, other_party, guest, other_guest):
        """Test the party.male_guest property."""
        assert party.male_guests == [guest]
        assert other_party.male_guests == []

    def test_female_guests(self, party, other_party, guest, other_guest):
        """Test the party.female_guest property."""
        assert party.female_guests == []
        assert other_party.female_guests == [other_guest]
