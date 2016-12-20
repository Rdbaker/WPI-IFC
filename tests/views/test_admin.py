# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import pytest

from tests.utils import BaseViewTest


class TestAdminViews(BaseViewTest):
    """Admin views tests."""
    endpoints = [
        '/admin/',
        '/admin/user/',
        '/admin/fraternity/',
        '/admin/party/',
        '/admin/preuser/',
    ]

    site_admin_only_endpoints = [
        '/admin/role/',
        '/admin/school/',
    ]

    site_admin_endpoints = endpoints + site_admin_only_endpoints

    @pytest.mark.parametrize('endpoint', site_admin_endpoints)
    def test_site_admin_endpoints(self, endpoint, site_admin, testapp):
        self.login(site_admin, testapp)
        res = testapp.get(endpoint)
        assert res.status_code == 200

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_admin_endpoints_accessible(self, endpoint, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get(endpoint)
        assert res.status_code == 200

    @pytest.mark.parametrize('endpoint', site_admin_only_endpoints)
    def test_site_admin_endpoints_inaccessible_to_admin(self, endpoint, admin,
                                                        testapp):
        self.login(admin, testapp)
        res = testapp.get(endpoint, status=404)
        assert res.status_code == 404

    @pytest.mark.parametrize('endpoint', site_admin_endpoints)
    def test_admin_endpoints_inaccessible_to_user(self, endpoint, user,
                                                  testapp):
        self.login(user, testapp)
        res = testapp.get(endpoint, status=404)
        assert res.status_code == 404

    @pytest.mark.parametrize('endpoint', site_admin_endpoints)
    def test_admin_endpoints_inaccessible_to_pres(self, endpoint, president,
                                                  testapp):
        self.login(president, testapp)
        res = testapp.get(endpoint, status=404)
        assert res.status_code == 404


class TestAdminContent(BaseViewTest):
    """Test that an admin only sees things about their school."""

    def test_user_view(self, testapp, admin, user, other_user,
                       other_school_user):
        self.login(admin, testapp)
        res = testapp.get('/admin/user/')
        assert admin.email in res
        assert user.email in res
        assert other_user.email in res
        assert other_school_user.email not in res

    def test_frat_view(self, testapp, admin, other_frat, other_school_frat):
        self.login(admin, testapp)
        res = testapp.get('/admin/fraternity/')
        assert admin.fraternity.title in res
        assert other_frat.title in res
        assert other_school_frat.title not in res

    def test_party_view(self, testapp, admin, other_school_party, party,
                        other_party):
        self.login(admin, testapp)
        res = testapp.get('/admin/party/')
        assert party.name in res
        assert other_party.name in res
        assert other_school_party.name not in res

    def test_preuser_view(self, testapp, admin, user, other_user,
                          other_school_user):
        self.login(admin, testapp)
        res = testapp.get('/admin/preuser/')
        assert admin.email in res
        assert user.email in res
        assert other_user.email in res
        assert other_school_user.email not in res
