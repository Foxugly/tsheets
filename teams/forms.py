from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm, CharField, TextInput

from .models import Team


class TeamForm(ModelForm):
    model = Team

    class Meta:
        model = Team
        fields = ['name', 'teamleaders', 'members', 'projects', 'deprecated']


class CreateTeamForm(BSModalModelForm):
    model = Team

    class Meta:
        model = Team
        fields = ['name', 'teamleaders', 'members', 'projects', 'deprecated']
