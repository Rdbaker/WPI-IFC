# -*- coding: utf-8 -*-
"""Admin models."""
from ifc.database import Column, Model, db



class Preuser(Model):
    """This is the model for users before they register.
    No validation because we're blindly trusting the data ingestion
    """
    __tablename__ = 'preusers'
    id = db.Column(db.Integer, primary_key=True)
    username = Column(db.String(80))
    #: The hashed password
    first_name = Column(db.String(30))
    last_name = Column(db.String(30))
    chapter_admin = Column(db.Boolean())
    ifc_admin = Column(db.Boolean())

    fraternity_name = Column(db.String(80))

    def __repr__(self):
        """Represent instance as a unique string."""
        return '<Pre-registered user: ({last_name}, {first_name})>'.format(
            last_name=self.last_name,
            first_name=self.first_name
        )
