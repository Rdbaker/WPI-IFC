# -*- coding: utf-8 -*-
"""Model unit tests."""
import random

import pytest

from ifc.constants import greek_letters
from ifc.models import Fraternity
from ifc.utils import InvalidAPIUsage


def generate_random_frats(k=120):
    """Create random fraternity names of 2 and 3 greek letters in length.

    I'm not sure how big this test should generally be to cover all the bases..
    but 120 seems like a good default.

    :param int: k (default: 120) -- this is the size of the sample to create
        for split between 2 and 3 letter names. I.e. 120 -> 60 2-letter names
        and 60 3-letter names

    :return list: a list containing k title-cased valid fraternity names
    """
    return (
        [' '.join(random.sample(greek_letters, 2)).title()
         for _ in range(k/2)] +
        [' '.join(random.sample(greek_letters, 3)).title()
         for _ in range(k/2)]
    )


@pytest.mark.usefixtures('db')
class TestFrat:
    """Fraternity tests."""
    @pytest.mark.parametrize('frat_title', generate_random_frats())
    def test_title_validation_no_errors(self, frat_title):
        assert Fraternity(title=frat_title, capacity=100)

    def test_title_validation_errors(self):
        with pytest.raises(InvalidAPIUsage):
            Fraternity(title='FIJI', capacity=10)
