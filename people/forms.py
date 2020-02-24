from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms

from people.models import Member


class MemberAddForm(forms.ModelForm):
    class Meta:
        model = Member
        exclude = ["active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit("submit", "Create Member"))
        self.helper.form_id = "add-form"
