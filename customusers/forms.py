from bootstrap_modal_forms.forms import BSModalModelForm
from django.contrib.auth.forms import UserChangeForm
from django.forms import ModelForm

from .models import CustomUser


class CustomUserForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            self.fields['is_superuser'].widget.attrs['readonly'] = True
            self.fields['is_superuser'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'language', 'hours_max', 'days_max', 'is_superuser', ]


class CustomUserFullForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(CustomUserFullForm, self).__init__(*args, **kwargs)
        self.fields['hours_max'].widget.attrs['class'] = 'positive'
        self.fields['days_max'].widget.attrs['class'] = 'positive'

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'language', 'hours_max', 'days_max', 'current_team', 'categories']


class CustomUserCreationForm(BSModalModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'language']


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("username", "email")
