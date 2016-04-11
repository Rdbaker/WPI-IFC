# -*- coding: utf-8 -*-
"""Party models."""
from sqlalchemy.orm import validates

from ifc.database import Column, Model, SurrogatePK, db, reference_col, relationship
from ifc.extensions import bcrypt
from ifc.constants import fraternityList

class Fraternity(SurrogatePK, Model):
    """A fraternity."""

    __tablename__ = 'fraternities'
    title = Column(db.String(80), unique=True, nullable=False)
    capacity = Column(db.Integer(), nullable=False)
    users = relationship('User')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Fraternity({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the fraternity."""
        assert title in fraternityList, 'Invalid Fraternity Name' + title
        return title
