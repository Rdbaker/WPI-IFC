# -*- coding: utf-8 -*-
"""Locales module. This constants for all strings to be shown."""


class Error(object):
    PARTY_DATE_IN_PAST = 'Must be after today, plan ahead.'
    FRAT_CANT_PARTY = "Your fraternity can't host parties right now."
    INVALID_FRAT_NAME = 'Invalid Fraternity Name'
    INVALID_FRAT_NAME_TEMPLATE = 'Invalid Fraternity Name: {}'
    PARTY_CREATOR_MISALIGNED = \
        'Party creator cannot belong to a different fraternity'
    PARTY_END_BEFORE_START = 'A party cannot end before it begins.'
    GUEST_NAME_SHORT = 'That guest needs a real name.'
    CANT_SEE_GUESTS = "You can't see the guests of this party"
    NOT_GUESTS_HOST = "You can't edit guests you didn't add"
    CANT_EDIT_GUESTS = "You can't edit the guests of this party"
    GUEST_REQUIRED_FIELDS = "name and is_male are required fields."
    GUEST_ALREADY_ON_LIST = 'That guest is already on this party list'
    UNKNOWN_USERNAME = 'Unknown username'
    INVALID_PW = 'Invalid password'
    USER_INACTIVE = 'User not activated'
    BAD_PW_VERIFICATION = 'Passwords must match'
    USERNAME_TAKEN = 'Username already registered'
    INVALID_ROLE = 'Invalid role title'


class Success(object):
    DATA_INGESTED = 'All data successfully ingested!'
    GUEST_DELETED = 'Successfully deleted guest'
    GUEST_CHECKED_IN = 'Successfully checked in guest'
    GUEST_CHECKED_OUT = 'Successfully checked out guest'
    LOGIN_SUCCESS = 'You are logged in.'
    LOGOUT_SUCCESS = 'You are logged out.'
    REGISTER_SUCCESS = 'Thank you for registering. You can now log in.'
    PARTY_CREATED = 'Party created.'


class FormConstants(object):
    USERNAME = 'Username'
    PASSWORD = 'Password'
    VERIFY_PW = 'Verify password'
    PARTY_NAME = 'Party Name'
    PARTY_DATE = 'Party Date'
