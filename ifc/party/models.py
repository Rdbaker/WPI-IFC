# -*- coding: utf-8 -*-
"""User models."""
from flask_login import UserMixin
from sqlalchemy.orm import validates

from ifc.database import Column, Model, SurrogatePK, db, reference_col, relationship
from ifc.extensions import bcrypt
from ifc.constants import fraternityList

class Fraternity(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'fraternities'
    title = Column(db.String(80), unique=True, nullable=False)
    capacity = Column(db.Integer(), nullable=False)

    def __init__(self, title, capacity, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, capacity=capacity, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Fraternity({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the role."""
        assert title in fraternityList, 'Invalid Fraternity Name'
        return title


class Fraternity(SurrogatePK, Model):
    """A role for a user."""

    __tablename__ = 'fraternities'
    title = Column(db.String(80), unique=True, nullable=False)
    capacity = Column(db.Integer(), nullable=False)

    def __init__(self, title, capacity, **kwargs):
        """Create instance."""
        db.Model.__init__(self, title=title, capacity=capacity, **kwargs)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Fraternity({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the role."""
        assert title in fraternityList, 'Invalid Fraternity Name'
        return title


