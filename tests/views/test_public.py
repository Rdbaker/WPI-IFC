# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
import os
import subprocess
import unittest

from flask import url_for

from ifc.user.models import User

from tests.utils import BaseViewTest


VERSION_DIR = os.path.join(os.getcwd(), "ifc")
VERSION_FILE = os.path.join(VERSION_DIR, "__init__.py")


MASTER_BRANCH = 'master'


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'example'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'example'
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for('public.logout')).follow()
        # sees alert
        assert 'You are logged out.' in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['email'] = user.email
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_email_doesnt_exist(self, user, testapp):
        """Show error if email doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['email'] = 'unknown'
        form['password'] = 'example'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown email' in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, preuser2, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get('/')
        # Clicks Create Account button
        res = res.click('Create account')
        # Fills out the form
        form = res.forms['registerForm']
        form['email'] = preuser2.email
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but passwords don't match
        form = res.forms['registerForm']
        form['email'] = 'foobar'
        form['password'] = 'secret'
        form['confirm'] = 'secrets'
        # Submits
        res = form.submit()
        # sees error message
        assert 'Passwords must match' in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        # Goes to registration page
        res = testapp.get(url_for('public.register'))
        # Fills out form, but email is already registered
        form = res.forms['registerForm']
        form['email'] = user.email
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Email already registered' in res


class TestHome(BaseViewTest):
    """Test the home page."""

    def test_get_without_login(self, frat, testapp):
        res = testapp.get('/')
        assert res.status_code == 200
        assert 'loginForm' in res.forms

    def test_get_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/')
        assert res.status_code == 200
        assert 'loginForm' not in res.forms

    def test_get_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/')
        assert res.status_code == 200
        assert 'loginForm' not in res.forms

    def test_get_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/')
        assert res.status_code == 200
        assert 'loginForm' not in res.forms


class TestNavbar(BaseViewTest):
    """Test the things in the navbar."""
    def test_admin_button_no_login(self, frat, testapp):
        res = testapp.get('/')
        assert 'href="/admin/"' not in res

    def test_admin_button_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/')
        assert 'href="/admin/"' not in res

    def test_admin_button_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/')
        assert 'href="/admin/"' not in res

    def test_admin_button_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/')
        assert 'href="/admin/"' in res

    def test_admin_button_as_site_admin(self, site_admin, testapp):
        self.login(site_admin, testapp)
        res = testapp.get('/')
        assert 'href="/admin/"' in res

    def test_ingest_button_no_login(self, frat, testapp):
        res = testapp.get('/')
        assert 'href="/ingest/"' not in res

    def test_ingest_button_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/')
        assert 'href="/ingest/"' not in res

    def test_ingest_button_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/')
        assert 'href="/ingest/"' not in res

    def test_ingest_button_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/')
        assert 'href="/ingest/"' in res

    def test_ingest_button_as_site_admin(self, site_admin, testapp):
        self.login(site_admin, testapp)
        res = testapp.get('/')
        assert 'href="/ingest/"' in res

    def test_change_frat_button_no_login(self, frat, testapp):
        res = testapp.get('/')
        assert 'href="/change-frat/' not in res

    def test_change_frat_button_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/')
        assert 'href="/change-frat/' not in res

    def test_change_frat_button_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/')
        assert 'href="/change-frat/' not in res

    def test_change_frat_button_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/')
        assert 'href="/change-frat/' not in res

    def test_change_frat_button_as_site_admin(self, site_admin, testapp):
        self.login(site_admin, testapp)
        res = testapp.get('/')
        assert 'href="/change-frat/' in res


class TestLogout(BaseViewTest):
    """Test the logout view."""

    def test_logout_without_login(self, frat, testapp):
        res = testapp.get('/logout/', status=401)
        assert res.status_code == 401

    def test_logout_as_user(self, user, testapp):
        self.login(user, testapp)
        res = testapp.get('/logout/')
        res = res.follow()
        assert 'You are logged out' in res

    def test_logout_as_pres(self, president, testapp):
        self.login(president, testapp)
        res = testapp.get('/logout/')
        res = res.follow()
        assert 'You are logged out' in res

    def test_logout_as_admin(self, admin, testapp):
        self.login(admin, testapp)
        res = testapp.get('/logout/')
        res = res.follow()
        assert 'You are logged out' in res


class TestRegister(BaseViewTest):
    """Tests the registering."""

    def test_register_no_preuser_fails(self, user, testapp):
        res = testapp.get(url_for('public.register'))
        form = res.forms['registerForm']
        form['email'] = 'something'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit(status=403)
        assert res.status_code == 403

    def test_register_with_preuser_works(self, preuser2, user, testapp):
        # NOTE: we ask for the "user" fixture so there's a role and fraternity
        # for the new user
        res = testapp.get(url_for('public.register'))
        form = res.forms['registerForm']
        form['email'] = preuser2.email
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'You can now log in' in res


class TestAbout:
    """Tests the about page."""

    def test_has_login_form(self, frat, testapp):
        res = testapp.get('/about/')
        assert 'loginForm' in res.forms

    def test_credit_where_its_due(self, frat, testapp):
        res = testapp.get('/about/')
        assert 'Ryan Baker' in res


class TestStatus:
    """Tests for the /status endpoint."""

    def test_has_correct_keys(self, testapp):
        res = testapp.get('/status')
        assert sorted(res.json.keys()) == ['version']

    def test_has_expected_values(self, testapp):
        res = testapp.get('/status')
        # NOTE: don't import the version and render it here, this process of
        # bumping the version should be very much on purpose
        assert res.json['version'] == '1.3.1'


class TestChangeFrat(BaseViewTest):
    """Tests the /change-frat/<id> endpoint."""

    def test_not_logged_in(self, testapp, frat):
        """Test that a not logged in user gets a 401."""
        res = testapp.get('/change-frat/1', status=401)
        assert res.status_code == 401

    def test_not_site_admin(self, testapp, admin):
        """Test that a non-site-admin gets a 403."""
        self.login(admin, testapp)
        res = testapp.get('/change-frat/1', status=403)
        assert res.status_code == 403

    def test_frat_not_found(self, testapp, site_admin):
        """Test that a fraternity that isn't found raises a 404."""
        self.login(site_admin, testapp)
        res = testapp.get('/change-frat/20', status=404)
        assert res.status_code == 404

    def test_successful_update(self, testapp, site_admin, other_frat):
        self.login(site_admin, testapp)
        assert site_admin.fraternity_id != other_frat.id
        res = testapp.get('/change-frat/{}'.format(other_frat.id)).follow()
        assert res.status_code == 200
        assert site_admin.fraternity_id == other_frat.id


class VersionTest(unittest.TestCase):

    def test_version_bump(self):
        repository_modified = (subprocess.call(['git', 'diff', '--quiet',
                                                MASTER_BRANCH]) == 1)
        if repository_modified:
            version_bumped = (subprocess.call(
                ['git', 'diff', '--quiet', MASTER_BRANCH, VERSION_FILE]) == 1)
            self.assertTrue(version_bumped,
                            "This repository has code changes from branch %s, "
                            "but %s is unchanged."
                            % (MASTER_BRANCH, VERSION_FILE))
