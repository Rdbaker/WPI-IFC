# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from ifc.app import create_app
from ifc.database import db as _db
from ifc.settings import TestConfig

from .factories import UserFactory, PreuserFactory, RoleFactory, FratFactory


@pytest.yield_fixture(scope='function')
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    """A database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def preuser(db):
    """A preuser for the tests."""
    return PreuserFactory.create()


@pytest.fixture
def preuser2(db):
    """A preuser for the tests."""
    return PreuserFactory.create()


@pytest.fixture
def frat(db):
    """A fraternity for the tests."""
    return FratFactory.create()


@pytest.fixture
def role(db):
    """A normal role for the tests."""
    return RoleFactory.create()


@pytest.fixture
def user(db, preuser, frat, role):
    """A user for the tests."""
    return UserFactory.create(username=preuser.username, password='myprecious',
                              role_id=role.id, fraternity_id=frat.id,
                              is_admin=False)


@pytest.fixture
def admin(db, preuser, frat):
    """An admin for the tests."""
    role = RoleFactory.create(title='ifc_admin')
    return UserFactory.create(username=preuser.username, password='myprecious',
                              role_id=role.id, fraternity_id=frat.id)


@pytest.fixture
def president(db, preuser, frat):
    """A chapter president for the tests."""
    role = RoleFactory.create(title='chapter_admin')
    return UserFactory.create(username=preuser.username, password='myprecious',
                              role_id=role.id, fraternity_id=frat.id)
