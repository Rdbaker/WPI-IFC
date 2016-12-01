# -*- coding: utf-8 -*-
"""Test forms."""
from datetime import date, timedelta as td
import mock

import pytest

from ifc.party.forms import NewPartyForm


@pytest.mark.usefixtures('db')
class TestNewPartyForm:
    """New party form."""

    @pytest.mark.parametrize('party_name', ['a', 'aa'] + ['a' * x
                                                          for x in range(36,
                                                                         40)])
    def test_invalid_length_name(self, party_name):
        """Party name too short."""
        form = NewPartyForm(name=party_name, date=date.today() + td(days=1))
        assert not form.validate()
        assert 'Field must be between' in form.name.errors[0]

    def test_name_required(self):
        """Party name is required."""
        form = NewPartyForm(name='', date=date.today() + td(days=1))
        assert not form.validate()
        assert 'This field is required.' in form.name.errors

    @pytest.mark.parametrize('party_name', ['a' * x for x in range(3, 36)])
    def test_valid_name(self, party_name, president):
        """Party name is ok length."""
        with mock.patch('ifc.party.forms.current_user') as cu_mock:
            cu_mock = president  # noqa
            form = NewPartyForm(name=party_name, date=date.today() + td(days=1))
            assert form.validate()
            assert form.name.errors == []

    def test_invalid_date(self):
        """Party date cannot be today, must be in future."""
        form = NewPartyForm(name='bleh', date=date.today())
        assert not form.validate()
        assert form.name.errors == []
        assert 'plan ahead' in form.date.errors[0]

    def test_frat_on_sopro(self):
        with mock.patch('ifc.party.forms.current_user') as cu_mock:
            cu_mock.fraternity = mock.Mock(can_have_parties=False)
            form = NewPartyForm(name='bleh', date=date.today() + td(days=1))
            assert not form.validate()
            assert "can't host parties" in form.name.errors[0]
