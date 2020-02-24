from django.views.generic import ListView, CreateView, DetailView

from events.models import Talk
from . import forms
from . import models


class MemberDetail(DetailView):
    model = models.Member
    slug_field = "pk"
    slug_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["talks"] = Talk.objects.filter(speaker=self.object).order_by("-date")
        return ctx


class MemberList(ListView):
    model = models.Member
    queryset = model.objects.filter(active=True)


class MemberAddView(CreateView):
    model = models.Member
    form_class = forms.MemberAddForm
