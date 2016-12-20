# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from datetime import date, timedelta as td

import mock
import pytest

from ifc import models as m

from tests.utils import BaseViewTest


class TestPartyListView(BaseViewTest):
    """Test the /parties/ endpoint."""
    def test_parties_without_login(self, frat, testapp):
        res = testapp.get('/parties/', status=401)
        assert res.status_code == 401

    def test_parties_as_user(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/')
        assert res.status_code == 200
        assert "{}'s Parties".format(user.fraternity.title) in res
        assert party.name in res

    def test_parties_as_pres(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/')
        assert res.status_code == 200
        assert "{}'s Parties".format(president.fraternity.title) in res
        assert party.name in res

    def test_parties_as_admin(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/')
        assert res.status_code == 200
        assert "{}'s Parties".format(admin.fraternity.title) in res
        assert party.name in res

    def test_pres_can_see_advanced_btns(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/')
        assert 'Start Party' in res
        assert 'Delete' in res

    def test_admin_can_see_advanced_btns(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/')
        assert 'Start Party' in res
        assert 'Delete' in res

    def test_user_cannot_see_advanced_btns(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/')
        assert 'Start Party' not in res
        assert 'Delete' not in res


class TestNewpartyView(BaseViewTest):
    """Test the /parties/new endpoint."""

    def test_new_without_login(self, frat, testapp):
        res = testapp.get('/parties/new', status=401)
        assert res.status_code == 401

    def test_new_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/new', status=403)
        assert res.status_code == 403

    def test_new_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/new')
        assert res.status_code == 200
        assert 'newPartyForm' in res.forms

    def test_parties_as_admin(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/new')
        assert res.status_code == 200
        assert 'newPartyForm' in res.forms


class TestCreatepartyView(BaseViewTest):
    """Tests the [POST] /parties/new endpoint."""
    def fill_form(self, testapp, name='My cool party!',
                  dt=(date.today() + td(days=1)).isoformat()):
        res = testapp.get('/parties/new')
        create_form = res.forms['newPartyForm']
        create_form['name'] = name
        create_form['date'] = dt
        return create_form

    def test_create_without_login(self, frat, testapp):
        res = testapp.post('/parties/new', status=401)
        assert res.status_code == 401

    def test_create_without_name(self, admin, testapp):
        self.login(admin, testapp)
        res = self.fill_form(testapp, name=None).submit()
        assert 'Party Name - This field is required.' in res

    def test_create_without_date(self, admin, testapp):
        self.login(admin, testapp)
        res = self.fill_form(testapp, dt=None).submit()
        assert 'Party Date - This field is required.' in res

    def test_create_for_yesterday(self, admin, testapp):
        self.login(admin, testapp)
        res = self.fill_form(testapp, dt=(date.today() - td(days=1))).submit()
        assert 'Party Date - Must be after today, plan ahead.' in res

    @pytest.mark.parametrize('pname',
                             ['a', 'aa'] + ['a' * x for x in range(36, 40)])
    def test_create_name_wrong(self, admin, pname, testapp):
        self.login(admin, testapp)
        res = self.fill_form(testapp, name=pname).submit()
        assert 'Party Name - Field must be between' in res

    def test_create_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.post('/parties/new', status=403)
        assert res.status_code == 403

    def test_create_as_president(self, president, testapp):
        self.login(president, testapp)
        old_len = len(m.Party.query.all())
        res = self.fill_form(testapp).submit().follow()
        assert res.status_code == 200
        assert len(m.Party.query.all()) == old_len + 1

    def test_create_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        old_len = len(m.Party.query.all())
        res = self.fill_form(testapp).submit().follow()
        assert res.status_code == 200
        assert len(m.Party.query.all()) == old_len + 1


class TestSinglePartyView(BaseViewTest):
    def test_no_login(self, frat, testapp):
        res = testapp.get('/parties/4', status=401)
        assert res.status_code == 401

    def test_user_can_view(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}'.format(party.id))
        assert user.fraternity.title + "'s Party" in res
        assert party.name in res

    def test_pres_can_view(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/{}'.format(party.id))
        assert president.fraternity.title + "'s Party" in res
        assert party.name in res

    def test_admin_can_view(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/{}'.format(party.id))
        assert admin.fraternity.title + "'s Party" in res
        assert party.name in res

    def test_other_user_cannot_view(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.get('/parties/{}'.format(party.id), status=403)
        assert res.status_code == 403

    def test_other_pres_cannot_view(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.get('/parties/{}'.format(party.id), status=403)
        assert res.status_code == 403

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/1', status=404)
        assert res.status_code == 404

    def test_party_post_calls_delete(self, user, party, testapp):
        with mock.patch('ifc.party.views.delete_party') as del_mock:
            self.login(user, testapp)
            del_mock.return_value = ('', 204,)
            res = testapp.post('/parties/{}'.format(party.id))
            assert res.status_code == 204
            del_mock.assert_called_with(party.id)


class TestReportView(BaseViewTest):
    """Tests the /parties/id/report endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.get('/parties/4/report', status=401)
        assert res.status_code == 401

    def test_user_can_view(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/report'.format(party.id))
        assert res.status_code == 200

    def test_pres_can_view(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/{}/report'.format(party.id))
        assert res.status_code == 200

    def test_admin_can_view(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/{}/report'.format(party.id))
        assert res.status_code == 200

    def test_other_user_cannot_view(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.get('/parties/{}/report'.format(party.id), status=403)
        assert res.status_code == 403

    def test_other_pres_cannot_view(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.get('/parties/{}/report'.format(party.id), status=403)
        assert res.status_code == 403

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/1', status=404)
        assert res.status_code == 404


class TestPartyEndStartView(BaseViewTest):
    """Tests the /parties/id/start endpoint."""
    endpoints = ['/parties/{}/start', '/parties/{}/end']

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_no_login(self, endpoint, frat, testapp):
        res = testapp.post(endpoint.format(4), status=401)
        assert res.status_code == 401

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_user_cannot_access(self, endpoint, user, testapp, party):
        self.login(user, testapp)
        res = testapp.post(endpoint.format(party.id), status=403)
        assert res.status_code == 403

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_pres_can_access(self, endpoint, president, testapp, party):
        self.login(president, testapp)
        res = testapp.post(endpoint.format(party.id)).follow()
        assert res.status_code == 200

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_admin_can_access(self, endpoint, admin, testapp, party):
        self.login(admin, testapp)
        res = testapp.post(endpoint.format(party.id)).follow()
        assert res.status_code == 200

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_other_user_cannot_access(self, endpoint, other_user, testapp,
                                      party):
        self.login(other_user, testapp)
        res = testapp.post(endpoint.format(party.id), status=403)
        assert res.status_code == 403

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_other_pres_cannot_access(self, endpoint, other_pres, testapp,
                                      party):
        self.login(other_pres, testapp)
        res = testapp.post(endpoint.format(party.id), status=403)
        assert res.status_code == 403

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_party_404(self, endpoint, user, testapp):
        self.login(user, testapp)
        res = testapp.post(endpoint.format(1), status=404)
        assert res.status_code == 404

    def test_start_and_end_party(self, admin, testapp, party):
        self.login(admin, testapp)
        assert not party.started
        assert not party.ended
        testapp.post('/parties/{}/start'.format(party.id))
        assert party.started
        assert not party.ended
        testapp.post('/parties/{}/end'.format(party.id))
        assert party.started
        assert party.ended

    def test_cannot_end_before_start(self, admin, testapp, party):
        """Tests that trying to end a party before it starts shows an error."""
        self.login(admin, testapp)
        assert not party.started
        assert not party.ended
        res = testapp.post('/parties/{}/end'.format(party.id)).follow()
        assert not party.started
        assert not party.ended
        assert 'cannot end' in res


class TestDeletePartyView(BaseViewTest):
    """Test the [DELETE] /parties/id endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.delete('/parties/1', status=401)
        assert res.status_code == 401

    def test_user_cannot_delete(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.delete('/parties/{}'.format(party.id), status=403)
        assert res.status_code == 403

    def test_other_user_cannot_delete(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.delete('/parties/{}'.format(party.id), status=403)
        assert res.status_code == 403

    def test_other_pres_cannot_delete(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.delete('/parties/{}'.format(party.id), status=403)
        assert res.status_code == 403

    def test_pres_can_delete(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.delete('/parties/{}'.format(party.id)).follow()
        assert res.status_code == 200

    def test_admin_can_delete(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.delete('/parties/{}'.format(party.id)).follow()
        assert res.status_code == 200

    def test_delete_removes_party(self, admin, party, testapp):
        self.login(admin, testapp)
        old_len = len(m.Party.query.all())
        testapp.delete('/parties/{}'.format(party.id))
        assert old_len == len(m.Party.query.all()) + 1

    def test_party_404(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.delete('/parties/1', status=404)
        assert res.status_code == 404


class TestGuestListView(BaseViewTest):
    """Tests the /parties/id/guests endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.get('/parties/1/guests', status=401)
        assert res.status_code == 401

    def test_user_can_access(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_pres_can_access(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_admin_can_access(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_other_user_cannot_access(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id), status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_other_pres_cannot_access(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id), status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/1/guests', status=404)
        assert res.status_code == 404

    def test_guest_list_returns_males_default(self, user, guest, party,
                                              testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests'.format(party.id))
        assert res.status_code == 200
        assert res.json['guests'] == map(lambda x: x.json_dict,
                                         party.male_guests)

    def test_guest_list_get_female_from_query(self, user, guest, party,
                                              testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests?is_male=false'.format(party.id))
        assert res.status_code == 200
        assert res.json['guests'] == map(lambda x: x.json_dict,
                                         party.female_guests)


class TestMenGuestListView(BaseViewTest):
    """Tests the /parties/id/guests/males endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.get('/parties/1/guests/males', status=401)
        assert res.status_code == 401

    def test_user_can_access(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_pres_can_access(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_admin_can_access(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_other_user_cannot_access(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id),
                          status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_other_pres_cannot_access(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id),
                          status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/1/guests/males', status=404)
        assert res.status_code == 404

    def test_guest_list_returns_males_only(self, user, guest, party,
                                           testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests/males'.format(party.id))
        assert res.status_code == 200
        assert res.json['guests'] == map(lambda x: x.json_dict,
                                         party.male_guests)


class TestWomenGuestListView(BaseViewTest):
    """Tests the /parties/id/guests/females endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.get('/parties/1/guests/females', status=401)
        assert res.status_code == 401

    def test_user_can_access(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_pres_can_access(self, president, party, testapp):
        self.login(president, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_admin_can_access(self, admin, party, testapp):
        self.login(admin, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id))
        assert res.status_code == 200
        assert res.json == {'guests': []}

    def test_other_user_cannot_access(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id),
                          status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_other_pres_cannot_access(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id),
                          status=403)
        assert res.status_code == 403
        assert res.json == {'error': "You can't see the guests of this party",
                            'message': 'You do not have permission to do that'}

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/1/guests/females', status=404)
        assert res.status_code == 404

    def test_guest_list_returns_males_only(self, user, guest, party,
                                           testapp):
        self.login(user, testapp)
        res = testapp.get('/parties/{}/guests/females'.format(party.id))
        assert res.status_code == 200
        assert res.json['guests'] == map(lambda x: x.json_dict,
                                         party.female_guests)


class TestDeleteGuestView(BaseViewTest):
    """Tests the [DELETE] /parties/id/guests/guest_id endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.delete('/parties/1/guests/1', status=401)
        assert res.status_code == 401

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.delete('/parties/1/guests/1', status=404)
        assert res.status_code == 404

    def test_guest_404(self, user, party, testapp):
        self.login(user, testapp)
        res = testapp.delete('/parties/{}/guests/1'.format(party.id),
                             status=404)
        assert res.status_code == 404

    def test_other_user_cant_access(self, other_user, party, guest, testapp):
        self.login(other_user, testapp)
        res = testapp.delete('/parties/{}/guests/{}'.format(party.id, guest.id),
                             status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit guests you didn't add"

    def test_other_pres_cant_access(self, other_pres, party, guest, testapp):
        self.login(other_pres, testapp)
        res = testapp.delete('/parties/{}/guests/{}'.format(party.id, guest.id),
                             status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit guests you didn't add"

    def test_host_can_delete_guest(self, user, guest, party, testapp):
        self.login(user, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.delete('/parties/{}/guests/{}'.format(party.id, guest.id))
        assert res.status_code == 204
        assert old_len == len(m.Guest.query.all()) + 1

    def test_admin_cannot_delete_guest(self, admin, guest, party, testapp):
        self.login(admin, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.delete('/parties/{}/guests/{}'.format(party.id, guest.id),
                             status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit guests you didn't add"
        assert old_len == len(m.Guest.query.all())


class TestGuestCreateView(BaseViewTest):
    """Tests [POST] /parties/id/guests endpoint."""
    def test_no_login(self, frat, testapp):
        res = testapp.post('/parties/1/guests', status=401)
        assert res.status_code == 401

    def test_party_404(self, user, testapp):
        self.login(user, testapp)
        res = testapp.post('/parties/1/guests', status=404)
        assert res.status_code == 404

    def test_other_user_cant_access(self, other_user, party, testapp):
        self.login(other_user, testapp)
        res = testapp.post('/parties/{}/guests'.format(party.id),
                           status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit the guests of this party"

    def test_other_pres_cant_access(self, other_pres, party, testapp):
        self.login(other_pres, testapp)
        res = testapp.post('/parties/{}/guests'.format(party.id),
                           status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit the guests of this party"

    def test_user_can_access(self, user, party, testapp):
        self.login(user, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': 'John Smith', 'is_male': True})
        assert res.status_code == 201
        assert res.json['guest']['name'] == 'John Smith'
        assert old_len == len(m.Guest.query.all()) - 1

    def test_pres_can_access(self, president, party, testapp):
        self.login(president, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': 'John Smith', 'is_male': True})
        assert res.status_code == 201
        assert res.json['guest']['name'] == 'John Smith'
        assert old_len == len(m.Guest.query.all()) - 1

    def test_admin_can_access(self, admin, party, testapp):
        self.login(admin, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': 'John Smith', 'is_male': True})
        assert res.status_code == 201
        assert res.json['guest']['name'] == 'John Smith'
        assert old_len == len(m.Guest.query.all()) - 1

    def test_guest_already_on_list(self, user, guest, party, testapp):
        self.login(user, testapp)
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': guest.name, 'is_male': True},
                                status=400)
        assert res.status_code == 400
        assert res.json['error'] == "That guest is already on this party list"

    @pytest.mark.parametrize('gname', ['', 'a', 'aa'])
    def test_guest_short_name(self, user, gname, party, testapp):
        self.login(user, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': gname, 'is_male': True},
                                status=422)
        assert res.status_code == 422
        assert res.json['error'] == "That guest needs a real name."
        assert old_len == len(m.Guest.query.all())

    def test_guest_no_gender(self, user, party, testapp):
        self.login(user, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'name': 'John Smith'},
                                status=400)
        assert res.status_code == 400
        assert res.json['error'] == "name and is_male are required fields."
        assert old_len == len(m.Guest.query.all())

    def test_guest_no_name(self, user, party, testapp):
        self.login(user, testapp)
        old_len = len(m.Guest.query.all())
        res = testapp.post_json('/parties/{}/guests'.format(party.id),
                                {'is_male': True},
                                status=400)
        assert res.status_code == 400
        assert res.json['error'] == "name and is_male are required fields."
        assert old_len == len(m.Guest.query.all())


class TestGuestCheckinView(BaseViewTest):
    """Tests the [PUT, PATCH] /parties/id/guests/guest_id endpoint."""
    methods = ['put', 'patch']

    @pytest.mark.parametrize('method_name', methods)
    def test_no_login(self, method_name, frat, testapp):
        res = getattr(testapp, method_name)('/parties/1/guests/1', status=401)
        assert res.status_code == 401

    @pytest.mark.parametrize('method_name', methods)
    def test_party_404(self, user, method_name, testapp):
        self.login(user, testapp)
        res = getattr(testapp, method_name)('/parties/1/guests/1', status=404)
        assert res.status_code == 404

    @pytest.mark.parametrize('method_name', methods)
    def test_guest_404(self, method_name, user, party, testapp):
        self.login(user, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/1'
                                            .format(party.id), status=404)
        assert res.status_code == 404

    @pytest.mark.parametrize('method_name', methods)
    def test_other_user_cant_access(self, method_name, other_user, party,
                                    testapp, guest):
        self.login(other_user, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/{}'
                                            .format(party.id, guest.id),
                                            status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit the guests of this party"

    @pytest.mark.parametrize('method_name', methods)
    def test_other_pres_cant_access(self, method_name, other_pres, party,
                                    testapp, guest):
        self.login(other_pres, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/{}'
                                            .format(party.id, guest.id),
                                            status=403)
        assert res.status_code == 403
        assert res.json['error'] == "You can't edit the guests of this party"

    @pytest.mark.parametrize('method_name', methods)
    def test_user_can_access(self, method_name, user, party, guest, testapp):
        self.login(user, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/{}'
                                            .format(party.id, guest.id))
        assert res.status_code == 202

    @pytest.mark.parametrize('method_name', methods)
    def test_pres_can_access(self, method_name, president, party, guest,
                             testapp):
        self.login(president, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/{}'
                                            .format(party.id, guest.id))
        assert res.status_code == 202

    @pytest.mark.parametrize('method_name', methods)
    def test_admin_can_access(self, method_name, admin, party, guest, testapp):
        self.login(admin, testapp)
        res = getattr(testapp, method_name)('/parties/{}/guests/{}'
                                            .format(party.id, guest.id))
        assert res.status_code == 202

    @pytest.mark.parametrize('method_name', methods)
    def test_checkin_and_out_guest(self, method_name, user, party, guest,
                                   testapp):
        self.login(user, testapp)
        assert not guest.is_at_party
        assert guest.entered_party_at is None
        assert guest.left_party_at is None
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        assert guest.is_at_party
        assert guest.entered_party_at is not None
        assert guest.left_party_at is None
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        assert not guest.is_at_party
        assert guest.entered_party_at is not None
        assert guest.left_party_at is not None
        assert guest.entered_party_at < guest.left_party_at

    @pytest.mark.parametrize('method_name', methods)
    def test_checkin_again_keeps_old_checkin_time(self, method_name, user,
                                                  party, guest, testapp):
        self.login(user, testapp)
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        old_checkin = guest.entered_party_at
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        old_checkout = guest.left_party_at
        # checkin again
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        assert guest.entered_party_at == old_checkin
        # checkout again
        getattr(testapp, method_name)('/parties/{}/guests/{}'
                                      .format(party.id, guest.id))
        assert guest.left_party_at == old_checkout
