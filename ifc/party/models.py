# -*- coding: utf-8 -*-
"""Party models."""
from datetime import datetime as dt

from sqlalchemy.orm import validates
from titlecase import titlecase

from ifc import locales
from ifc.database import Column, Model, SurrogatePK, db, reference_col, \
    relationship
from ifc.constants import fraternityList


class Fraternity(SurrogatePK, Model):
    """A fraternity."""

    __tablename__ = 'fraternities'
    title = Column(db.String(80), unique=True, nullable=False)
    capacity = Column(db.Integer(), nullable=False)
    users = relationship('User')
    parties = relationship('Party', cascade='delete', single_parent=True)
    can_have_parties = Column(db.Boolean(), default=True, nullable=False)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Fraternity({title})>'.format(title=self.title)

    @validates('title')
    def validate_title(self, key, title):
        """Validate the title of the fraternity."""
        assert title in fraternityList, \
            locales.Error.INVALID_FRAT_NAME_TEMPLATE.format(title)
        return title


class Party(SurrogatePK, Model):
    """A party for a fraternity."""

    __tablename__ = 'parties'
    name = Column(db.String(80), nullable=False)
    date = Column(db.Date(), nullable=False)
    started = Column(db.Boolean(), nullable=False, default=False)
    ended = Column(db.Boolean(), nullable=False, default=False)
    creator_id = reference_col('users', nullable=False)
    creator = relationship('User')
    fraternity_id = reference_col('fraternities', nullable=False)
    fraternity = relationship('Fraternity')
    guests = relationship('Guest', cascade='delete', single_parent=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Party({name})>'.format(name=self.name)

    @validates('fraternity', 'creator')
    def validate_fraternity(self, key, field):
        """Ensures that the creator is part of the fraternity"""
        if key is 'creator' and self.fraternity is not None:
            assert field.fraternity == self.fraternity, \
                locales.Error.PARTY_CREATOR_MISALIGNED
        elif key is 'fraternity' and self.creator is not None:
            assert self.creator.fraternity == field, \
                locales.Error.PARTY_CREATOR_MISALIGNED
        return field

    def is_on_guest_list(self, guest_name):
        """Validates whether or not the guest is on the party list."""
        return guest_name.lower() in [guest.name.lower()
                                      for guest in self.guests]

    @property
    def male_guests(self):
        """Get the male guests"""
        return [guest for guest in self.guests if guest.is_male]

    @property
    def female_guests(self):
        """Get the female guests"""
        return [guest for guest in self.guests if not guest.is_male]

    def start(self):
        """Let's get it started"""
        self.started = True
        self.save()

    def end(self):
        """Ok, that's enough PARTY'S OVER."""
        assert self.started, locales.Error.PARTY_END_BEFORE_START
        self.ended = True
        self.save()


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
    entered_party_at = Column(db.DateTime)
    left_party_at = Column(db.DateTime)
    __table_args__ = (db.UniqueConstraint('name', 'party_id',
                                          name='_name_party_uc'),)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Guest({name} at {party})>'.format(name=self.name,
                                                   party=self.party.name)

    @validates('name')
    def validate_name(self, key, field):
        """Ensures that the guest is not already added to the party list"""
        assert len(field) > 3, locales.Error.GUEST_NAME_SHORT
        return field.lower()

    @property
    def json_dict(self):
        """Returns the guest as a JSON serializable python dict."""
        return {'name': titlecase(self.name), 'host': self.host.full_name,
                'is_male': self.is_male, 'is_at_party': self.is_at_party,
                'id': self.id, 'left_at': self.left_party_at,
                'entered_at': self.entered_party_at}

    def leave_party(self):
        """The logic for a guest leaving the party."""
        self.is_at_party = False
        if self.left_party_at is None:
            self.left_party_at = dt.utcnow()
        self.save()

    def enter_party(self):
        """The logic for a guest entering a party."""
        self.is_at_party = True
        if self.entered_party_at is None:
            self.entered_party_at = dt.utcnow()
        self.save()
