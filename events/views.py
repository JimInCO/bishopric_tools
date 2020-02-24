from django.views.generic import CreateView, DetailView, ListView, UpdateView
from django_xhtml2pdf.views import PdfMixin

from . import models
from . import forms


class TalkDetail(DetailView):
    model = models.Talk
    slug_field = "id"
    slug_url_kwarg = "id"


class TalkPdfDetail(PdfMixin, TalkDetail):
    template_name = "events/pdf.html"


class TalkAdd(CreateView):
    model = models.Talk
    form_class = forms.TalkForm

    def get_initial(self):
        init = super(TalkAdd, self).get_initial()
        # Copy the dictionary so we don't accidentally change a mutable dict
        initial = init.copy()
        initial["speaker"] = self.request.GET.get("member", None)
        return initial


class TalkEdit(UpdateView):
    model = models.Talk
    form_class = forms.TalkForm
    slug_field = "id"
    slug_url_kwarg = "id"

    def get_form_kwargs(self):
        values = super(TalkEdit, self).get_form_kwargs()
        values["button"] = "Update Talk"
        return values


class TalkList(ListView):
    model = models.Talk

    def get_queryset(self):
        qs = super().get_queryset()
        qs = qs.order_by("date", "order")
        return qs
