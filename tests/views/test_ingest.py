# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from tests.utils import BaseViewTest


class TestIngestViews(BaseViewTest):
    """Ingest views tests."""

    def test_ingest_get_inaccessible_to_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/ingest/', status=403)
        assert res.status_code == 403

    def test_ingest_get_inaccessible_not_logged_in(self, testapp):
        res = testapp.get('/ingest/', status=401)
        assert res.status_code == 401

    def test_ingest_get_inaccessible_to_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/ingest/', status=403)
        assert res.status_code == 403

    def test_ingest_get_accessible_to_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/ingest/')
        assert res.status_code == 200

    def test_ingest_post_inaccessible_to_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.post('/ingest/', status=403)
        assert res.status_code == 403

    def test_ingest_post_inaccessible_not_logged_in(self, testapp):
        res = testapp.post('/ingest/', status=401)
        assert res.status_code == 401

    def test_ingest_post_inaccessible_to_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.post('/ingest/', status=403)
        assert res.status_code == 403

    def test_ingest_post_accessible_to_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.post('/ingest/')
        assert res.status_code == 200
