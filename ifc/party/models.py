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
    parties = relationship('Party')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Fraternity({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the fraternity."""
        assert title in fraternityList, 'Invalid Fraternity Name' + title
        return title


class Party(SurrogatePK, Model):
    """A party for a fraternity."""

    __tablename__ = 'parties'
    name = Column(db.String(80), nullable=False)
    date = Column(db.Date(), nullable=False)
    creator_id = reference_col('users', nullable=False)
    creator = relationship('User')
    fraternity_id = reference_col('fraternities', nullable=False)
    fraternity = relationship('Fraternity')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Party({name})>'.format(name=self.name)

    @validates('fraternity', 'creator')
    def validate_fraternity(self, key, field):
        """Ensures that the creator is part of the fraternity"""
        if self.creator is not None and self.fraternity is not None:
            assert self.creator.fraternity == self.fraternity, 'Party creator cannot belong to a different fraternity'
        return field
