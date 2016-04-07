# -*- coding: utf-8 -*-
"""User models."""
from flask_login import UserMixin
from sqlalchemy.orm import validates

from ifc.database import Column, Model, SurrogatePK, db, reference_col, relationship
from ifc.extensions import bcrypt


class Role(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'roles'
    title = Column(db.String(80), unique=True, nullable=False)
    users = relationship('User')

    def __init__(self, title, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Role({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the role."""
        assert title in ['ifc_admin', 'chapter_admin', 'normal'], 'Invalid role title'
        return title


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    username = Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    role_id = reference_col('roles', nullable=False)
    role = relationship('Role')

    def __init__(self, username, password=None, **kwargs):
        """Create instance."""
        role = Role.query.filter(Role.title == 'normal').first()
        db.Model.__init__(self, username=username, role=role, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def email(self):
        """User email derived from username."""
        return '{0}@wpi.edu'.format(self.username)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({username})>'.format(username=self.username)
