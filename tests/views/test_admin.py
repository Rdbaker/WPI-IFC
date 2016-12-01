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
        '/admin/role/',
    ]

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_admin_endpoints_accessible(self, endpoint, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get(endpoint)
        assert res.status_code == 200

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_admin_endpoints_inaccessible_to_user(self, endpoint, user,
                                                  testapp):
        self.login(user, testapp)
        print(user.role)
        res = testapp.get(endpoint, status=401)
        assert res.status_code == 401

    @pytest.mark.parametrize('endpoint', endpoints)
    def test_admin_endpoints_inaccessible_to_pres(self, endpoint, president,
                                                  testapp):
        self.login(president, testapp)
        print(president.role)
        res = testapp.get(endpoint, status=401)
        assert res.status_code == 401
