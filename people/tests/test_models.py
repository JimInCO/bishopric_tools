import pytest

from people.tests.factories import MemberFactory
from django.utils import timezone

year = timezone.now().year
pytestmark = pytest.mark.django_db


def test_member_get_absolute_url():
    member = MemberFactory()
    assert member.get_absolute_url() == f"/members/{member.pk}/"


def test_sister_name():
    member = MemberFactory(gender=0)
    assert member.formal_name == f"Sister {member.last_name}"


def test_brother_name():
    member = MemberFactory(gender=1)
    assert member.formal_name == f"Brother {member.last_name}"


def test_youth():
    member = MemberFactory(birth_year=(year - 15))
    assert member.adult is False


def test_adult():
    member = MemberFactory(birth_year=2001)
    assert member.adult is True
