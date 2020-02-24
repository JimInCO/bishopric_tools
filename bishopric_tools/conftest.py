import pytest
from django.test import RequestFactory

from bishopric_tools.users.models import User
from bishopric_tools.users.tests.factories import UserFactory
from people.models import Member
from people.tests.factories import MemberFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def member() -> Member:
    """
    Wrapper for a Member object. Meant to simplify testing of the Member model.
    """
    return MemberFactory()


@pytest.fixture
def request_factory() -> RequestFactory:
    return RequestFactory()
