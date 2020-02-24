import pytest

from events.tests.factories import TalkFactory

pytestmark = pytest.mark.django_db


def test_talk_get_absolute_url():
    talk = TalkFactory()
    assert talk.get_absolute_url() == f"/talks/{talk.pk}/"
