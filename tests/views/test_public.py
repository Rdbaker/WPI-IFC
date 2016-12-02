# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from flask import url_for

from ifc.user.models import User

from tests.utils import BaseViewTest


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
        form['password'] = 'example'
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get('/')
        # Fills out login form in navbar
        form = res.forms['loginForm']
        form['username'] = user.username
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
        form['username'] = user.username
        form['password'] = 'wrong'
        # Submits
        res = form.submit()
        # sees error
        assert 'Invalid password' in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get('/')
        # Fills out login form, password incorrect
        form = res.forms['loginForm']
        form['username'] = 'unknown'
        form['password'] = 'example'
        # Submits
        res = form.submit()
        # sees error
        assert 'Unknown user' in res


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
        form['username'] = preuser2.username
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
        form['username'] = 'foobar'
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
        # Fills out form, but username is already registered
        form = res.forms['registerForm']
        form['username'] = user.username
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        # Submits
        res = form.submit()
        # sees error
        assert 'Username already registered' in res


class TestHome(BaseViewTest):
    """Test the home page."""

    def test_get_without_login(self, testapp):
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


class TestLogout(BaseViewTest):
    """Test the logout view."""

    def test_logout_without_login(self, testapp):
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
        form['username'] = 'something'
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit(status=403)
        assert res.status_code == 403

    def test_register_with_preuser_works(self, preuser2, user, testapp):
        # NOTE: we ask for the "user" fixture so there's a role and fraternity
        # for the new user
        res = testapp.get(url_for('public.register'))
        form = res.forms['registerForm']
        form['username'] = preuser2.username
        form['password'] = 'secret'
        form['confirm'] = 'secret'
        res = form.submit().follow()
        assert res.status_code == 200
        assert 'You can now log in' in res


class TestAbout:
    """Tests the about page."""

    def test_has_login_form(self, testapp):
        res = testapp.get('/about/')
        assert 'loginForm' in res.forms

    def test_credit_where_its_due(self, testapp):
        res = testapp.get('/about/')
        assert 'Ryan Baker' in res
