# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from ifc.database import db
from ifc.user.models import User, Preuser, Role, Fraternity


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    password = PostGenerationMethodCall('set_password', 'example')
    active = True

    class Meta:
        """Factory configuration."""

        model = User


class PreuserFactory(BaseFactory):
    """Preuser factory."""

    username = Sequence(lambda n: 'user{0}'.format(n))
    first_name = Sequence(lambda n: 'first name {0}'.format(n))
    last_name = Sequence(lambda n: 'last name {0}'.format(n))
    fraternity_name = 'Sigma Pi'

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
