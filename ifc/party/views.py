# -*- coding: utf-8 -*-
"""Party views."""
from functools import partial

from flask import Blueprint, render_template, request, flash, redirect, \
    url_for, jsonify, g
from flask_login import login_required, current_user
from sqlalchemy.exc import IntegrityError

from . import forms
from .models import Party, Guest
from .report import Report
from ifc import locales
from ifc.utils import flash_errors, InvalidAPIUsage, permission_required

blueprint = Blueprint('parties', __name__, url_prefix='/parties',
                      static_folder='../static')


@blueprint.route('/')
@login_required
def parties():
    """List the parties."""
    return render_template('party/list.html',
                           parties=sorted(list(current_user.fraternity.parties),
                                          key=lambda x: x.date, reverse=True))


@blueprint.route('/new', methods=['GET'])
@permission_required('can_create_party')
def newparty():
    """Form to create a new party."""
    return render_template('party/new.html', form=forms.NewPartyForm())


@blueprint.route('/new', methods=['POST'])
@permission_required('can_create_party')
def createparty():
    form = forms.NewPartyForm(request.form)
    if form.validate_on_submit():
        Party.create(
            name=form.name.data,
            date=form.date.data,
            fraternity=current_user.fraternity,
            creator=current_user)
        flash(locales.Success.PARTY_CREATED, 'success')
        return redirect(url_for('parties.parties'))
    else:
        flash_errors(form)
        return render_template('party/new.html', form=form)


@blueprint.route('/<int:party_id>', methods=['GET', 'POST'])
@permission_required('can_view_party_by_id', apply_req_args=True)
def guest_list(party_id):
    if request.method == 'POST':
        return delete_party(party_id)
    else:
        return render_template('party/guests.html', party=g.party)


@blueprint.route('/<int:party_id>/report', methods=['GET'])
@permission_required('can_view_party_by_id', apply_req_args=True)
def show_report(party_id):
    return render_template('report/index.html', party=g.party)


@blueprint.route('/<int:party_id>/report/data', methods=['GET'])
@permission_required('can_view_party_by_id', apply_req_args=True)
def report_data(party_id):
    report = Report(g.party)
    return jsonify(attendance=report.attendance,
                   total_guests=report.total_guests,
                   population=report.population_buckets,
                   attendance_ratio=report.attendance_ratio,
                   host_attendance_raw=report.host_attendance_raw,
                   host_attendance_normalized=report.host_attendance_normalized,
                   attendance_raw=report.attendance_raw,
                   gender_population=report.gendered_population_buckets)


@blueprint.route('/<int:party_id>/start', methods=['POST'])
@permission_required('can_delete_party_by_id', apply_req_args=True)
def start_party(party_id):
    g.party.start()
    return redirect(url_for('parties.parties'))


@blueprint.route('/<int:party_id>/end', methods=['POST'])
@permission_required('can_delete_party_by_id', apply_req_args=True)
def end_party(party_id):
    try:
        g.party.end()
    except AssertionError as ex:
        flash(ex.message, 'danger')
    return redirect(url_for('parties.parties'))


@blueprint.route('/<int:party_id>', methods=['DELETE'])
@permission_required('can_delete_party_by_id', apply_req_args=True)
def delete_party(party_id):
    g.party.delete()
    return redirect(url_for('parties.parties'))


@blueprint.route('/<int:party_id>/guests', methods=['GET'])
@permission_required('can_view_party_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.CANT_SEE_GUESTS}))
def get_guest_list(party_id):
    if 'is_male' in request.args:
        is_male = request.args.get('is_male', 'true').lower()
        if is_male == 'true':
            guests = g.party.male_guests
        else:
            guests = g.party.female_guests
    else:
        guests = g.party.guests
    return jsonify(guests=[gu.json_dict for gu in guests])


@blueprint.route('/<int:party_id>/guests/males', methods=['GET'])
@permission_required('can_view_party_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.CANT_SEE_GUESTS}))
def get_men_guest_list(party_id):
    return jsonify(guests=[gu.json_dict for gu in g.party.male_guests])


@blueprint.route('/<int:party_id>/guests/females', methods=['GET'])
@permission_required('can_view_party_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.CANT_SEE_GUESTS}))
def get_women_guest_list(party_id):
    return jsonify(guests=[gu.json_dict for gu in g.party.female_guests])


@blueprint.route('/<int:party_id>/guests/<int:guest_id>', methods=['DELETE'])
@permission_required('can_edit_guest_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.NOT_GUESTS_HOST}))
def delete_guest_from_list(party_id, guest_id):
    if g.party.ended:
        raise InvalidAPIUsage(status_code=409,
                              payload={'error':
                                       locales.Error.PARTY_ENDED_DELETE_GUEST})
    g.guest.delete()
    res = jsonify(message=locales.Success.GUEST_DELETED)
    res.status_code = 204
    return res


@blueprint.route('/<int:party_id>/guests', methods=['POST'])
@permission_required('can_view_party_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.CANT_EDIT_GUESTS}))
def add_guest(party_id):
    if g.party.ended:
        raise InvalidAPIUsage(status_code=409,
                              payload={'error':
                                       locales.Error.PARTY_ENDED_ADD_GUEST})
    try:
        capacity = current_user.party_capacity
        if capacity is not None:
            is_male = request.json['is_male']
            guest_count = Guest.query.filter_by(
                host=current_user,
                party=g.party,
                is_male=is_male).count()
            if is_male and capacity.male_max is not None and \
                    guest_count >= capacity.male_max:
                raise InvalidAPIUsage(
                    payload={'error':
                             'You can only add {} guys to the party'.format(
                                 capacity.male_max)})
            elif not is_male and capacity.female_max is not None and \
                    guest_count >= capacity.female_max:
                raise InvalidAPIUsage(
                    payload={'error':
                             'You can only add {} girls to the party'.format(
                                 capacity.female_max)})
        guest = Guest.create(name=request.json['name'].lower(),
                             host=current_user,
                             party=g.party,
                             is_male=request.json['is_male'])
        res = jsonify(guest=guest.json_dict)
        res.status_code = 201
        return res
    except KeyError:
        raise InvalidAPIUsage(payload={'error':
                                       locales.Error.GUEST_REQUIRED_FIELDS})
    except IntegrityError:
        raise InvalidAPIUsage(payload={'error':
                                       locales.Error.GUEST_ALREADY_ON_LIST})


@blueprint.route('/<int:party_id>/guests/<int:guest_id>',
                 methods=['PUT', 'PATCH'])
@permission_required('can_view_party_by_id', apply_req_args=True,
                     fail_exc=partial(InvalidAPIUsage, status_code=403,
                                      payload={'error':
                                               locales.Error.CANT_EDIT_GUESTS}))
def switch_guest_occupancy(party_id, guest_id):
    if g.party.ended:
        raise InvalidAPIUsage(status_code=409,
                              payload={'error':
                                       locales.Error.PARTY_ENDED_CHECKIN_GUEST})
    guest = Guest.find_or_404(guest_id)
    if guest.is_at_party:
        guest.leave_party()
    else:
        guest.enter_party()
    if guest.is_at_party:
        message = locales.Success.GUEST_CHECKED_IN
    else:
        message = locales.Success.GUEST_CHECKED_OUT
    res = jsonify(message=message)
    res.status_code = 202
    return res
