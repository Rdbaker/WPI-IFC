# -*- coding: utf-8 -*-
"""Report logic class."""
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
        rate = (float(len([g
                           for g in guests
                           if g.entered_party_at is not None])) /
                float(len(guests)))
        return rate

    @cached_property
    def population_buckets(self, ):
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

        guests = self.party.guests
        enter_times = sorted([g.entered_party_at
                              for g in guests
                              if g.entered_party_at is not None])
        left_times = sorted([g.left_party_at
                             for g in guests
                             if g.left_party_at is not None])
        first_bucket = round_down_from_interval(enter_times[0])
        last_bucket = round_down_from_interval(left_times[-1])

        buckets = []

        bucket_delta = datetime.timedelta(minutes=minute_bucket_interval)
        # initialize all the buckets from start to end
        while first_bucket <= last_bucket:
            buckets.append(
                {'time': first_bucket.isoformat(),
                 'population': get_population_for_bucket(first_bucket)}
            )
            first_bucket += bucket_delta

        return buckets
