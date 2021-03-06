# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from datetime import date, timedelta as td
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from ifc.database import db
from ifc.models import User, Preuser, Role, Fraternity, Party, Guest, School, \
    Capacity


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session
        force_flush = True


class UserFactory(BaseFactory):
    """User factory."""

    email = Sequence(lambda n: 'user{0}@test.com'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class PreuserFactory(BaseFactory):
    """Preuser factory."""

    email = Sequence(lambda n: 'user{0}@test.com'.format(n))
    first_name = Sequence(lambda n: 'first_name_{0}'.format(n))
    last_name = Sequence(lambda n: 'last_name_{0}'.format(n))
    fraternity_name = 'Sigma Pi'
    school_title = 'Worcester Polytechnic Institute'

    class Meta:
        """Factory configuration."""

        model = Preuser


class RoleFactory(BaseFactory):
    title = 'normal'

    class Meta:
        model = Role


class FratFactory(BaseFactory):

    title = 'Sigma Pi'
    capacity = 100

    class Meta:
        model = Fraternity


class PartyFactory(BaseFactory):

    name = 'Cool Party, Bro'
    date = date.today() + td(days=1)

    class Meta:
        model = Party


class GuestFactory(BaseFactory):
    name = Sequence(lambda n: 'guest {0}'.format(n))
    is_male = True

    class Meta:
        model = Guest


class SchoolFactory(BaseFactory):
    title = 'Worcester Polytechnic Institute'
    short_title = 'WPI'

    class Meta:
        model = School


class CapacityFactory(BaseFactory):
    male_max = 1
    female_max = 1

    class Meta:
        model = Capacity
