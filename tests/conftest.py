# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import pytest
from webtest import TestApp

from ifc.app import create_app
from ifc.database import db as _db
from ifc.settings import TestConfig

from .factories import UserFactory, PreuserFactory, RoleFactory, FratFactory, \
    PartyFactory, GuestFactory, SchoolFactory


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
def other_preuser(db):
    """A preuser for another fraternity."""
    return PreuserFactory.create(fraternity_name='Zeta Psi')


@pytest.fixture
def preuser2(db):
    """A preuser for the tests."""
    return PreuserFactory.create()


@pytest.fixture
def admin_preuser(db, frat):
    return PreuserFactory.create(ifc_admin=True)


@pytest.fixture
def pres_pre(db, frat):
    return PreuserFactory.create(chapter_admin=True)


@pytest.fixture
def other_pres_pre(db, other_frat):
    return PreuserFactory.create(chapter_admin=True,
                                 fraternity_name=other_frat.title)


@pytest.fixture
def school(db):
    """A school for the tests."""
    return SchoolFactory.create()


@pytest.fixture
def other_school(db):
    """Another school for the tests."""
    return SchoolFactory.create(title='Northeastern University',
                                short_title='NEU')


@pytest.fixture
def frat(db, school):
    """A fraternity for the tests."""
    return FratFactory.create(school=school, school_id=school.id)


@pytest.fixture
def other_frat(db, school):
    """Another fraternity for tests."""
    return FratFactory.create(title='Zeta Psi', school_id=school.id)


@pytest.fixture
def role(db):
    """A normal role for the tests."""
    return RoleFactory.create()


@pytest.fixture
def pres_role(db):
    """A president role for the tests."""
    return RoleFactory.create(title='chapter_admin')


@pytest.fixture
def admin_role(db):
    """An admin role for the tests."""
    return RoleFactory.create(title='ifc_admin')


@pytest.fixture
def user(db, preuser, frat, role):
    """A user for the tests."""
    return UserFactory.create(email=preuser.email)


@pytest.fixture
def other_user(db, other_preuser, other_frat, role):
    """Another fraternity for tests."""
    return UserFactory.create(email=other_preuser.email)


@pytest.fixture
def admin(db, admin_preuser, frat, admin_role):
    """An admin for the tests."""
    return UserFactory.create(email=admin_preuser.email)


@pytest.fixture
def president(db, pres_pre, frat, pres_role):
    """A chapter president for the tests."""
    return UserFactory(email=pres_pre.email)


@pytest.fixture
def other_pres(db, other_pres_pre, other_frat, pres_role):
    """A president of another chapter for the tests."""
    return UserFactory.create(email=other_pres_pre.email)


@pytest.fixture
def party(db, frat, president):
    """A party for the tests."""
    return PartyFactory.create(fraternity=frat,
                               creator=president)


@pytest.fixture
def other_party(db, other_frat, other_pres):
    """A party from another frat."""
    return PartyFactory.create(fraternity=other_frat,
                               creator=other_pres)


@pytest.fixture
def guest(db, user, party):
    """A guest for the tests."""
    return GuestFactory.create(host=user,
                               host_id=user.id,
                               party=party,
                               party_id=party.id)


@pytest.fixture
def other_guest(db, other_user, other_party):
    """A guest from another party for the tests."""
    return GuestFactory.create(host=other_user,
                               host_id=other_user.id,
                               party=other_party,
                               is_male=False,
                               party_id=other_party.id)
