# -*- coding: utf-8 -*-
"""School models."""

from ifc.database import Column, Model, SurrogatePK, db, relationship


class School(SurrogatePK, Model):
    """A school for an implementation of this software."""

    __tablename__ = 'schools'
    title = Column(db.String(120), unique=True, nullable=False)
    short_title = Column(db.String(10))
    fraternities = relationship('Fraternity', cascade='delete',
                                single_parent=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<School({title})>'.format(title=self.title)

    @property
    def abbreviation(self):
        return self.short_title

    @property
    def frats(self):
        return self.fraternities
