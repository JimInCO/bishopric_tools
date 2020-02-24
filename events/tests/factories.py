import datetime

from factory import DjangoModelFactory, LazyFunction, SubFactory

from events.models import Talk
from people.tests.factories import MemberFactory


class TalkFactory(DjangoModelFactory):
    class Meta:
        model = Talk

    speaker = SubFactory(MemberFactory)
    date = LazyFunction(datetime.date.today)
    bishopric = "Bishop\n1st Counselor\n2nd Counselor"
