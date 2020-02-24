from datetime import date

from django.db import models
from django.urls import reverse
from model_utils import Choices

from events.models import Talk


class Member(models.Model):
    GENDER = Choices((0, "female", "female"), (1, "male", "male"))
    lds_id = models.CharField(max_length=11, unique=True)
    gender = models.IntegerField(choices=GENDER)
    first_name = models.CharField(max_length=30, verbose_name="First name")
    last_name = models.CharField(max_length=40, verbose_name="Last name")
    birth_year = models.PositiveIntegerField(verbose_name="Birth Year")

    # Contact information
    email = models.EmailField(verbose_name="E-Mail", blank=True, null=True)
    phone = models.CharField(max_length=20, verbose_name="Phone Number", blank=True, null=True)
    street1 = models.CharField(max_length=50)
    street2 = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=60)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=10, blank=True, null=True)

    # Still in the ward
    active = models.BooleanField(default=True)

    # Notes
    notes = models.TextField(blank=True)

    @property
    def full_name(self):
        """Returns the person's full name"""
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def formal_name(self):
        """Returns the person's Title (Brother/Sister) and last name"""
        if self.gender == 0:
            return "Sister {}".format(self.last_name)
        else:
            return "Brother {}".format(self.last_name)

    @property
    def age(self):
        """Returns the person's age"""
        return int((date.today().year - self.birth_year))

    @property
    def adult(self):
        return self.age >= 19

    @property
    def last_talk_date(self):
        talks = Talk.objects.filter(speaker=self).order_by("-date")
        if len(talks) > 0:
            return talks[0].date
        else:
            return None

    def get_absolute_url(self):
        return reverse("members:detail", args=[str(self.pk)])

    def __str__(self):
        return self.full_name
