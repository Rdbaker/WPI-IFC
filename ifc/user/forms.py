# -*- coding: utf-8 -*-
"""User forms."""
from flask_wtf import Form
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, EqualTo, Length

from ifc import locales

from .models import User


class RegisterForm(Form):
    """Register form."""

    email = StringField(locales.FormConstants.EMAIL,
                        validators=[DataRequired(), Length(min=3, max=25)])
    password = PasswordField(locales.FormConstants.PASSWORD,
                             validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField(
        locales.FormConstants.VERIFY_PW,
        [DataRequired(),
         EqualTo('password', message=locales.Error.BAD_PW_VERIFICATION)])

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = User.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append(locales.Error.EMAIL_TAKEN)
            return False
        return True
