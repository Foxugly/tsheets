from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm, CharField, TextInput

from .models import Holiday


class HolidayForm(ModelForm):
    model = Holiday
    day = CharField(widget=TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Holiday
        fields = ['day', ]


class CreateHolidayForm(BSModalModelForm):
    model = Holiday
    day = CharField(widget=TextInput(attrs={'type': 'date'}))

    class Meta:
        model = Holiday
        fields = ['day', ]
