from ajax_select.fields import AutoCompleteSelectField
from crispy_forms.bootstrap import AppendedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Column
from django import forms

from . import models


class TalkForm(forms.ModelForm):
    speaker = AutoCompleteSelectField("members", required=True, help_text=None, plugin_options={"minLength": 2})
    reference_materials = forms.CharField(
        label="Reference Materials", widget=forms.Textarea(attrs={"rows": 2}), required=False,
    )
    bishopric = forms.CharField(
        label="Bishopric",
        widget=forms.Textarea(attrs={"rows": 4}),
        initial=models.Talk._meta.get_field("bishopric").default,
        required=True,
    )
    date = forms.DateField(input_formats=["%d %b %Y"],)

    class Meta:
        model = models.Talk
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        button = kwargs.pop("button", "Create Talk")
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", button))
        self.helper.form_id = "add-form"
        self.helper.layout = Layout(
            Row(
                Column("speaker", css_class="form-group col-6 mb-0"),
                AppendedText(
                    "date", '<i class="fa fa-calendar" aria-hidden="true"></i>', active=True, wrapper_class="col-6",
                ),
                css_class="form-row",
            ),
            Row(
                Column("time_range", css_class="form-group col-6 mb-0"),
                Column("order", css_class="form-group col-6 mb-0"),
                css_class="form-row",
            ),
            "topic",
            "reference_materials",
            "bishopric",
        )
