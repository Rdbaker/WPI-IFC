# -*- coding: utf-8 -*-
"""Manage views."""
from flask import Blueprint, render_template, g, request, redirect, url_for

from flask_login import current_user

from ifc.models import User, Role
from ifc.utils import permission_required
from .models import Capacity

blueprint = Blueprint('manage', __name__, url_prefix='/manage',
                      static_folder='../static')


def update_capacity(user, male_max, female_max):
    """Update the capacity for a user."""
    capacity = user.party_capacity
    if capacity is None:
        new_capacity = Capacity.create(male_max=male_max,
                                       female_max=female_max)
        user.party_capacity = new_capacity
        user.save()
    else:
        user.party_capacity.update(male_max=male_max,
                                   female_max=female_max)


@blueprint.route('/brother-guest-capacity')
@permission_required('can_manage_fraternity')
def guest_capacity():
    """Manage the brothers of the fraternity."""
    return render_template('manage/brother_capacity.html',
                           brothers=current_user.fraternity.users,
                           roles=Role.query.all())


@blueprint.route('/bulk-brother-guest-capacity', methods=['POST'])
@permission_required('can_manage_fraternity')
def bulk_update_brother_guest_capacity():
    """Update capacities in bulk for roles of a fraternity."""
    role = Role.find_or_404(request.form.get('role_id', 0, int))
    male_max = request.form.get('male_max', None, int)
    female_max = request.form.get('female_max', None, int)
    for user in User.query.filter_by(fraternity_id=current_user.fraternity_id,
                                     role_id=role.id).all():
        update_capacity(user, male_max, female_max)
    return redirect(url_for('manage.guest_capacity'))


@blueprint.route('/brother-guest-capacity/<int:brother_id>', methods=['POST'])
@permission_required('can_manage_brother_by_id', apply_req_args=True)
def update_brother_guest_capacity(brother_id):
    """Manage the guest capacity of the brother."""
    male_max = request.form.get('male_max', None, int)
    female_max = request.form.get('female_max', None, int)
    update_capacity(g.brother, male_max, female_max)
    return redirect(url_for('manage.guest_capacity'))
