# -*- coding: utf-8 -*-
"""Party views."""
from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from werkzeug.exceptions import Forbidden

from . import forms
from .models import Party, Guest
from ifc.utils import flash_errors

blueprint = Blueprint('party', __name__, url_prefix='/parties', static_folder='../static')


@blueprint.route('/')
@login_required
def parties():
    """List the parties."""
    return render_template('party/list.html', parties=sorted(current_user.fraternity.parties, key=lambda x: x.date, reverse=True))


@blueprint.route('/new', methods=['GET'])
@login_required
def newparty():
    """Form to create a new party."""
    if current_user.can_create_party:
        return render_template('party/new.html', form=forms.NewPartyForm(user=current_user))
    else:
        raise Forbidden()


@blueprint.route('/new', methods=['POST'])
@login_required
def createparty():
    if current_user.can_create_party:
        form = forms.NewPartyForm(request.form)
        if form.validate_on_submit():
            party = Party.create(
                name=form.name.data,
                date=form.date.data,
                fraternity=current_user.fraternity,
                creator=current_user)
            flash('Party created.', 'success')
            return redirect(url_for('party.parties'))
        else:
            flash_errors(form)
            return render_template('party/new.html', form=form)
    else:
        raise Forbidden()


@blueprint.route('/<int:id>', methods=['GET', 'POST'])
@login_required
def guest_list(id):
    if request.method == 'POST':
        return delete_party(id)
    else:
        party = Party.find_by_id(id)
        if current_user.can_view_party(party):
            return render_template('party/guests.html', party=party)
        else:
            raise Forbidden()


@blueprint.route('/<int:id>/start', methods=['POST'])
@login_required
def start_party(id):
    party = Party.find_by_id(id)
    if current_user.can_delete_party(party):
        party.start()
        return redirect(url_for('party.parties'))
    else:
        raise Forbidden()


@blueprint.route('/<int:id>', methods=['DELETE'])
@login_required
def delete_party(id):
    party = Party.find_by_id(id)
    if current_user.can_delete_party(party):
        party.delete()
        return redirect(url_for('party.parties'))
    else:
        raise Forbidden()


@blueprint.route('/<int:id>/guests', methods=['GET'])
@login_required
def get_guest_list(id):
    party = Party.find_by_id(id)
    if current_user.can_view_party(party):
        is_male = request.args.get('is_male', 'true').lower()
        guests = party.male_guests if is_male == 'true' else party.female_guests
        return jsonify(guests=[g.json_dict for g in guests])
    else:
        res = jsonify(error="You can't see the guests of this party")
        res.status_code = 403
        return res


@blueprint.route('/<int:party_id>/guests/<int:guest_id>', methods=['DELETE'])
@login_required
def delete_guest_from_list(party_id, guest_id):
    party = Party.find_by_id(party_id)
    if current_user.can_view_party(party):
        guest = Guest.find_by_id(guest_id)
        if guest.host == current_user:
            guest.delete()
            res = jsonify(message="Successfully deleted guest")
            res.status_code = 204
            return res
        else:
            res = jsonify(error="You can't edit guests you didn't add")
            res.status_code = 403
            return res
    else:
        res = jsonify(error="You can't edit the guests of this party")
        res.status_code = 403
        return res


@blueprint.route('/<int:party_id>/guests', methods=['POST'])
@login_required
def add_guest(party_id):
    party = Party.find_by_id(party_id)
    if current_user.can_view_party(party):
        try:
            guest = Guest.create(name=request.json['name'].lower(),
                                 host=current_user,
                                 party=party,
                                 is_male=request.json['is_male'])
            res = jsonify(guest=guest.json_dict)
            res.status_code = 201
            return res
        except AssertionError as e:
            res = jsonify(error=e.message)
            res.status_code = 400
            return res
    else:
        res = jsonify(error="You can't edit the guests of this party")
        res.status_code = 403
        return res


@blueprint.route('/<int:party_id>/guests/<int:guest_id>', methods=['PUT', 'PATCH'])
@login_required
def switch_guest_occupancy(party_id, guest_id):
    party = Party.find_by_id(party_id)
    if current_user.can_view_party(party):
        guest = Guest.find_by_id(guest_id)
        guest.is_at_party = not guest.is_at_party
        guest.save()
        message = "Successfully checked in guest" if guest.is_at_party else "Successfully checked out guest"
        res = jsonify(message=message)
        res.status_code = 202
        return res
    else:
        res = jsonify(error="You can't edit the guests of this party")
        res.status_code = 403
        return res
