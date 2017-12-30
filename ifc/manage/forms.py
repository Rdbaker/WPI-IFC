# -*- coding: utf-8 -*-
"""Party forms."""
from flask_wtf import Form
from wtforms import IntegerField


class CapacityForm(Form):
    """Capacity form."""

    male_max = IntegerField()
    female_max = IntegerField()
