# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from tests.utils import BaseViewTest


class TestUserViews(BaseViewTest):
    """User views tests."""

    def test_me_endpoint(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/users/me')
        assert res.status_code == 200
        assert res.json == {'me': user.json_dict}

    def test_root_endpoint_redirects_to_parties(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/users/')
        assert '/parties/' in res.body
        assert res.follow()

    def test_unauth_me_endpoint(self, testapp):
        assert testapp.get('/users/me', status=401)

    def test_unauth_root_endpoint(self, testapp):
        assert testapp.get('/users/', status=401)
