# -*- coding: utf-8 -*-
"""Report logic class."""
import collections
import datetime

from cached_property import cached_property

from .models import Party


class Report(object):
    def __init__(self, party):
        """Create a new report from the given party.
        The report will have standard statistics that are pre-computed
        as well as more advanced figures from on-the-fly calculations.

        :param Party: party -- The party model from which a report should be
            derived

        example usage:
            >>> from ifc.party.report import Report
            >>> from ifc.models import Party
            >>> p = Party.query.first()
            >>> r = Report(p)
            >>> r
            <Report(...)>

        Raises:
            TypeError -- if the supplied parameter is not of type `Party`
        """
        if not isinstance(party, Party):
            raise TypeError("The 'party' parameter must be of type Party")
        self.party = party

    @cached_property
    def total_guests(self):
        """Return a simple count of the guests."""
        return len(self.party.guests)

    @cached_property
    def attendance(self):
        """Return the attendance of the party as a percentage of the number of
        guests who showed up to the party.

        :return float: A float x <= 1 representing the percentage of guests who
            at some point checked in to the party

        example usage:
            >>> from ifc.party.report import Report
            >>> from ifc.models import Party
            >>> p = Party.query.first()
            >>> r = Report(p)
            >>> r.attendance
            0.8

        The above example would mean that 80% of the guests on the list showed
        up to the party at some point.

        This is computed by the equation:

            (guests who were checked in) / (total guests)
        """
        guests = self.party.guests

        if not guests:
            return 0.0

        rate = (float(len([g
                           for g in guests
                           if g.entered_party_at is not None])) /
                float(len(guests)))
        return rate

    @cached_property
    def gendered_population_buckets(self):
        minute_bucket_interval = 10
        guests = self.party.guests

        # if there are no guests, just return
        if not guests:
            return []

        def round_down_from_interval(dt):
            """Given some datetime object, round it down (in minutes) to the
            nearest interval given the variable (in the scope)
            minute_bucket_interval."""
            return dt - datetime.timedelta(
                minutes=dt.minute % minute_bucket_interval,
                seconds=dt.second,
                microseconds=dt.microsecond)

        def get_population_for_bucket(dt, is_male):
            """Given some time bucket, find the number of guests who were
            checked in to the party at that time."""
            in_attendance = 0

            entered_before = dt + datetime.timedelta(minutes=10)
            left_after = dt

            # for each guest
            for guest in guests:
                # if the guest entered some point before the end of this bucket
                if guest.entered_party_at is not None and \
                        guest.entered_party_at <= entered_before:
                    # if the guest left sometime after the start of this bucket
                    # (or never left)
                    if guest.left_party_at is None or \
                            guest.left_party_at > left_after:
                        # they were at the party
                        if (is_male and guest.is_male) or \
                                (not is_male and not guest.is_male):
                            in_attendance += 1
            return in_attendance

        male_enter_times = sorted([g.entered_party_at
                                   for g in guests
                                   if g.entered_party_at is not None and
                                   g.is_male])
        male_left_times = sorted([g.left_party_at
                                  for g in guests
                                  if g.left_party_at is not None and
                                  g.is_male])
        female_enter_times = sorted([g.entered_party_at
                                     for g in guests
                                     if g.entered_party_at is not None and
                                     not g.is_male])
        female_left_times = sorted([g.left_party_at
                                    for g in guests
                                    if g.left_party_at is not None and
                                    not g.is_male])

        if (not male_enter_times or not male_left_times) and \
                (not female_enter_times or not female_left_times):
            return []

        male_first_bucket = round_down_from_interval(male_enter_times[0])
        male_last_bucket = round_down_from_interval(male_left_times[-1])
        female_first_bucket = round_down_from_interval(female_enter_times[0])
        female_last_bucket = round_down_from_interval(female_left_times[-1])

        gender_buckets = {
            'male': [],
            'female': [],
        }

        bucket_delta = datetime.timedelta(minutes=minute_bucket_interval)
        # initialize all the buckets from start to end
        while male_first_bucket <= male_last_bucket:
            gender_buckets['male'].append(
                {'time': male_first_bucket.isoformat() + 'Z',
                 'population': get_population_for_bucket(male_first_bucket, True)}
            )
            male_first_bucket += bucket_delta

        while female_first_bucket <= female_last_bucket:
            gender_buckets['female'].append(
                {'time': female_first_bucket.isoformat() + 'Z',
                 'population': get_population_for_bucket(female_first_bucket, False)}
            )
            female_first_bucket += bucket_delta

        return gender_buckets

    @cached_property
    def population_buckets(self):
        """Returns a data structure of bucketed population on the granularity
        of 10 minutes.

        The data structure is an array of dicts with 2 keys: 'time' and
        'population'. The array is sorted (ascending) by the 'time' key.

        This is how the data structure is shaped:
            [
                {'time': '2016-12-20T22:00:00.0000Z', 'population': 2},
                {'time': '2016-12-20T22:10:00.0000Z', 'population': 3},
                {'time': '2016-12-20T22:20:00.0000Z', 'population': 7},
                {'time': '2016-12-20T22:30:00.0000Z', 'population': 18},
                ...
                {'time': '2016-12-21T01:30:00.0000Z', 'population': 1},
            ]
        """
        minute_bucket_interval = 10
        guests = self.party.guests

        # if there are no guests, just return
        if not guests:
            return []

        def round_down_from_interval(dt):
            """Given some datetime object, round it down (in minutes) to the
            nearest interval given the variable (in the scope)
            minute_bucket_interval."""
            return dt - datetime.timedelta(
                minutes=dt.minute % minute_bucket_interval,
                seconds=dt.second,
                microseconds=dt.microsecond)

        def get_population_for_bucket(dt):
            """Given some time bucket, find the number of guests who were
            checked in to the party at that time."""
            in_attendance = 0

            entered_before = dt + datetime.timedelta(minutes=10)
            left_after = dt

            # for each guest
            for guest in guests:
                # if the guest entered some point before the end of this bucket
                if guest.entered_party_at is not None and \
                        guest.entered_party_at <= entered_before:
                    # if the guest left sometime after the start of this bucket
                    # (or never left)
                    if guest.left_party_at is None or \
                            guest.left_party_at > left_after:
                        # they were at the party
                        in_attendance += 1
            return in_attendance

        enter_times = sorted([g.entered_party_at
                              for g in guests
                              if g.entered_party_at is not None])
        left_times = sorted([g.left_party_at
                             for g in guests
                             if g.left_party_at is not None])

        if not enter_times or not left_times:
            return []

        first_bucket = round_down_from_interval(enter_times[0])
        last_bucket = round_down_from_interval(left_times[-1])

        buckets = []

        bucket_delta = datetime.timedelta(minutes=minute_bucket_interval)
        # initialize all the buckets from start to end
        while first_bucket <= last_bucket:
            buckets.append(
                {'time': first_bucket.isoformat() + 'Z',
                 'population': get_population_for_bucket(first_bucket)}
            )
            first_bucket += bucket_delta

        return buckets

    @cached_property
    def attendance_raw(self):
        return {
            'girls_who_showed': len([g for g in self.party.guests
                                     if g.entered_party_at is not None
                                     and not g.is_male]),
            'guys_who_showed': len([g for g in self.party.guests
                                    if g.entered_party_at is not None
                                    and g.is_male]),
            'girls_who_didnt_show': len([g for g in self.party.guests
                                         if g.entered_party_at is None
                                         and not g.is_male]),
            'guys_who_didnt_show': len([g for g in self.party.guests
                                        if g.entered_party_at is None
                                        and g.is_male]),
        }

    @cached_property
    def attendance_ratio(self):
        """Calculate the ratio of girls who showed up to guys who showed up.

        :return dict: The response will be a dict shaped like this:
            {'women': 1.252,
             'men': 1.0}
            representing the ratio of men to women in attendance of the party.
        """
        female_attended = len([g for g in self.party.female_guests
                               if g.entered_party_at is not None])
        male_attended = len([g for g in self.party.male_guests
                             if g.entered_party_at is not None])
        if not male_attended:
            return {'men': 1.0, 'women': 1.0}

        return {'men': 1.0,
                'women': float(female_attended)/float(male_attended)}

    @cached_property
    def host_attendance_raw(self):
        """Calculate who got the most people to show up. Does not take in to
        account the number of people they put on the list, just the number of
        guests under their name who showed up.

        :return [tuple]: a list of tuples that each have two elements: a full
            name of a brother and the number of guests that checked in to the
            party that were under their name. E.g. [('Ryan Baker', 201), ...]
        """
        return collections.Counter([g.host.full_name
                                    for g in self.party.guests
                                    if g.entered_party_at is not None]).items()

    @cached_property
    def host_attendance_normalized(self):
        """Calculate the ratio of <guests added>:<guests attended> per host.

        :return [tuple]: a list of tuples that each have two elements: a full
            name of a brother and the ratio of guests they added to the list
            versus guests that were checked in to the party.
        """
        return [
            (t[0],
             float(t[1]) /
             len(filter(lambda g: g.host.full_name == t[0], self.party.guests)))
            for t in self.host_attendance_raw
        ]
