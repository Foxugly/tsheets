from bootstrap_modal_forms.forms import BSModalModelForm
from django.core.exceptions import ValidationError
from django.forms import ModelForm, CharField, TextInput

from days.models import Day
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

    def clean_day(self):
        """Reject usernames that differ only in case."""
        day = self.cleaned_data.get("day")
        if self._meta.model.objects.filter(day=day).exists():
            self._update_errors(
                ValidationError(
                    {
                        "day": self.instance.unique_error_message(self._meta.model, ["day"])
                    }
                )
            )
        else:
            return day

    class Meta:
        model = Holiday
        fields = ['day', ]
