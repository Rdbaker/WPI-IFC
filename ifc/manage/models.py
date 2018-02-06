# -*- coding: utf-8 -*-
"""Manage models."""
from ifc.database import Column, Model, SurrogatePK, db


class Capacity(SurrogatePK, Model):
    """A capacity for a brother."""

    __tablename__ = 'capacities'
    male_max = Column(db.Integer(), nullable=True)
    female_max = Column(db.Integer(), nullable=True)

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Capacity(m[{}] | f[{}])>'.format(self.male_max,
                                                  self.female_max)
