from django.db import models
from django.urls import reverse
from model_utils.models import TimeStampedModel


class Talk(TimeStampedModel):
    speaker = models.ForeignKey("people.Member", on_delete=models.CASCADE)
    date = models.DateField()
    topic = models.CharField(max_length=150, blank=True, null=True)
    time_range = models.CharField(max_length=10, blank=True, null=True)
    reference_materials = models.TextField("Reference Materials", blank=True, null=True)

    bishopric = models.TextField("Bishopric", default="Kelly Ericson\nJames McDonald\nWilliam Clayton")
    order = models.IntegerField("Speaker Order", blank=True, null=True)

    def __str__(self):
        return "{} on {}".format(self.speaker.full_name, self.date)

    def get_absolute_url(self):
        return reverse("talks:talk-detail", args=[str(self.pk)])


class SacramentMeeting(models.Model):
    date = models.DateField()

    def __str__(self):
        return "Sacrament Meeting on {}".format(self.date)
