# -*- coding: utf-8 -*-
"""Party forms."""
from datetime import date

from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length


class NewPartyForm(Form):
    """New Party form."""

    name = StringField('Party Name',
                       validators=[DataRequired(), Length(min=3, max=35)])
    date = DateField('Party Date', validators=[DataRequired()])

    def __init__(self, user, *args, **kwargs):
        """Create instance."""
        super(NewPartyForm, self).__init__(*args, **kwargs)
        self.user = user

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewPartyForm, self).validate()
        if not initial_validation:
            return False
        if not date.today() < self.date.data:
            self.date.errors.append('Must be after today, plan ahead.')
            return False
        if not current_user.fraternity.can_have_parties:
            self.name.errors.append('Your fraternity can\'t host parties right now.')
            return False

        return True
