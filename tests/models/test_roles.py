# -*- coding: utf-8 -*-
"""Model unit tests."""
import pytest

from ifc.user.models import Role


@pytest.mark.usefixtures('db')
class TestRole:
    """Role tests."""
    @pytest.mark.parametrize('role_title', ['ifc_admin', 'chapter_admin',
                                            'normal'])
    def test_title_validation_no_errors(self, role_title):
        assert Role(title=role_title)

    def test_title_validation_errors(self):
        with pytest.raises(AssertionError):
            Role(title='bad role')
