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
    guests = relationship('Guest')

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Party({name})>'.format(name=self.name)

    @validates('fraternity', 'creator')
    def validate_fraternity(self, key, field):
        """Ensures that the creator is part of the fraternity"""
        if self.creator is not None and self.fraternity is not None:
            assert self.creator.fraternity == self.fraternity, 'Party creator cannot belong to a different fraternity'
        return field

    def is_on_guest_list(self, guest_name):
        """Validates whether or not the guest is on the party list."""
        return guest_name.lower() in [guest.name.lower() for guest in self.guests]

    @property
    def male_guests(self):
        """Get the male guests"""
        return [guest for guest in self.guests if guest.is_male]

    @property
    def female_guests(self):
        """Get the female guests"""
        return [guest for guest in self.guests if not guest.is_male]


class Guest(SurrogatePK, Model):
    """A guest for a party"""

    __tablename__ = 'guests'

    name = Column(db.String(80), nullable=False)
    host_id = reference_col('users', nullable=False)
    host = relationship('User')
    party_id = reference_col('parties', nullable=False)
    party = relationship('Party')
    is_at_party = Column(db.Boolean(), default=False, nullable=False)
    is_male = Column(db.Boolean(), nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Guest({name} at {party})>'.format(name=self.name, party=self.party.name)

    @validates('name', 'party')
    def validate_name_unique_to_party(self, key, field):
        """Ensures that the guest is not already added to the party list"""
        if not (self.name is None and self.party is None):
            if key == 'name':
                assert not self.party.is_on_guest_list(field), 'That guest is already on this party list'
                assert len(field) > 3, 'That guest needs a real name.'
        return field

    @property
    def json_dict(self):
        """Returns the guest as a JSON serializable python dict."""
        return { 'name': self.name.title(), 'host': self.host.full_name, 'is_male': self.is_male, 'is_at_party': self.is_at_party, 'id': self.id }
