# -*- coding: utf-8 -*-
"""Party forms."""
from datetime import date

from flask_wtf import Form
from flask_login import current_user
from wtforms import StringField, DateField
from wtforms.validators import DataRequired, Length

from ifc import locales


class NewPartyForm(Form):
    """New Party form."""

    name = StringField(locales.FormConstants.PARTY_NAME,
                       validators=[DataRequired(), Length(min=3, max=35)])
    date = DateField(locales.FormConstants.PARTY_DATE,
                     validators=[DataRequired()])

    def validate(self):
        """Validate the form."""
        initial_validation = super(NewPartyForm, self).validate()
        if not initial_validation:
            return False
        if not date.today() < self.date.data:
            self.date.errors.append(locales.Error.PARTY_DATE_IN_PAST)
            return False
        if not current_user.fraternity.can_have_parties:
            self.name.errors.append(locales.Error.FRAT_CANT_PARTY)
            return False

        return True
