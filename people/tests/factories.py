from factory import DjangoModelFactory, Sequence
from factory.fuzzy import FuzzyInteger
from django.utils import timezone

from people.models import Member

year = timezone.now().year


class MemberFactory(DjangoModelFactory):
    class Meta:
        model = Member

    birth_year = FuzzyInteger(year - 90, year - 12)

    # Contact information
    gender = FuzzyInteger(0, 1)
    phone = Sequence(lambda n: "720%07d" % n)
    city = "Broomfield"
    state = "CO"
    zip_code = "80020"

    # Still in the ward
    active = True
