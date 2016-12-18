# -*- coding: utf-8 -*-
"""User models."""
import flask
from flask_login import UserMixin
from sqlalchemy.orm import validates
from werkzeug.exceptions import Forbidden

from ifc import locales
from ifc.database import Column, Model, SurrogatePK, db, reference_col, \
    relationship
from ifc.extensions import bcrypt
from ifc.admin.models import Preuser
from ifc.party.models import Fraternity, Party, Guest


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
        assert title in ['ifc_admin', 'chapter_admin', 'normal'], \
            locales.Error.INVALID_ROLE
        return title


class User(UserMixin, SurrogatePK, Model):
    """A user of the app."""

    __tablename__ = 'users'
    email = Column(db.String(100), unique=True, nullable=False)
    username = Column(db.String(80), nullable=False)
    #: The hashed password
    password = Column(db.String(128), nullable=True)
    first_name = Column(db.String(30), nullable=True)
    last_name = Column(db.String(30), nullable=True)
    active = Column(db.Boolean(), default=False)
    is_admin = Column(db.Boolean(), default=False)
    role_id = reference_col('roles', nullable=False)
    role = relationship('Role')

    fraternity_id = reference_col('fraternities', nullable=False)
    fraternity = relationship('Fraternity')

    parties = relationship('Party', cascade='delete', single_parent=True)

    def __init__(self, email, password=None, **kwargs):
        """Create instance."""
        pre = Preuser.query.filter(Preuser.email == email).first()
        if pre is None:
            raise Forbidden()

        role = self.resolve_role_from_preuser(pre)
        if role is None and 'role_id' in kwargs:
            role = Role.find_by_id(kwargs['role_id'])

        fraternity = self.resolve_frat_from_preuser(pre)
        if fraternity is None and 'fraternity_id' in kwargs:
            fraternity = Fraternity.find_by_id(kwargs['fraternity_id'])

        # create the user
        db.Model.__init__(
            self,
            email=email,
            role=role,
            fraternity=fraternity,
            first_name=pre.first_name,
            last_name=pre.last_name)
        if password:
            self.set_password(password)
        else:
            self.password = None
        self.active = True

    def set_password(self, password):
        """Set password."""
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        """Check password."""
        return bcrypt.check_password_hash(self.password, value)

    def resolve_role_from_preuser(self, pre):
        """Figures out what the role is from the preregistered-user model."""
        if pre.ifc_admin:
            return Role.query.filter(Role.title == 'ifc_admin').first()
        elif pre.chapter_admin:
            return Role.query.filter(Role.title == 'chapter_admin').first()
        else:
            return Role.query.filter(Role.title == 'normal').first()

    def resolve_frat_from_preuser(self, pre):
        """Finds the fraternity from the preregistered-user model."""
        return Fraternity.query.filter(
            Fraternity.title == pre.fraternity_name,
            Fraternity.school.title == pre.school_title).first()

    @property
    def full_name(self):
        """Full user name."""
        return '{0} {1}'.format(self.first_name, self.last_name)

    @property
    def username(self):
        """Username derived from email."""
        return self.email.split('@')[0]

    @property
    def is_site_admin(self):
        """True if the user is a site admin."""
        return self.role.title == 'ifc_admin'

    @property
    def is_chapter_admin(self):
        """True if the user is a chapter admin."""
        return self.role.title == 'chapter_admin'

    @property
    def school_name(self):
        """Gets the shortened school name if there is one, otherwise returns
        the full name."""
        if self.fraternity.school.short_title is not None:
            return self.fraternity.school.short_title
        else:
            return self.fraternity.school.title

    def can_delete_party_by_id(self, party_id):
        """True if the user can delete the given party."""
        party = Party.find_or_404(party_id)
        flask.g.party = party
        return self.can_delete_party(party)

    def can_delete_party(self, party):
        """True if the user can delete the given party."""
        return self.is_site_admin or (self.is_chapter_admin and
                                      self.fraternity == party.fraternity)

    @property
    def can_create_party(self):
        """True if the user can create a party."""
        return self.is_site_admin or self.is_chapter_admin

    def can_view_party_by_id(self, party_id, guest_id=None):
        """True if the user can view the given party."""
        party = Party.find_or_404(party_id)
        if guest_id is not None:
            guest = Guest.find_or_404(guest_id)
            flask.g.guest = guest
        flask.g.party = party
        return self.can_view_party(party)

    def can_view_party(self, party):
        """True if the user can view the guest list of a party"""
        return self.is_site_admin or party.fraternity == self.fraternity

    def can_edit_guest_by_id(self, guest_id, party_id=None):
        """True if the user can edit the guest."""
        guest = Guest.find_or_404(guest_id)
        if party_id is not None:
            party = Party.find_or_404(party_id)
            flask.g.party = party
        flask.g.guest = guest
        return self.can_edit_guest(guest)

    def can_edit_guest(self, guest):
        """True if the user can edit the guest."""
        return guest.host == self

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<User({email})>'.format(email=self.email)

    @property
    def json_dict(self):
        """Represent the instance as a dict that can be converted to JSON."""
        return {'username': self.username, 'first_name': self.first_name,
                'last_name': self.last_name, 'full_name': self.full_name,
                'id': self.id}
