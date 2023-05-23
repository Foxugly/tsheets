from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm

from .models import Week


class WeekForm(ModelForm):
    model = Week

    class Meta:
        model = Week
        fields = ['weekdate']


class CreateWeekForm(BSModalModelForm):
    model = Week

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Week
        fields = ['weekdate']
