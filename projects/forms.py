from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm, Textarea, CharField

from projects.models import Project


class ProjectForm(ModelForm):
    model = Project
    description = CharField(widget=Textarea(), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categories'].widget.attrs['multiple'] = 'multiple'

    class Meta:
        model = Project
        fields = ['name', 'description', 'refer_team', 'categories', 'deprecated']


class CreateProjectForm(BSModalModelForm):
    model = Project
    description = CharField(widget=Textarea(), required=False)

    class Meta:
        model = Project
        fields = ['name', 'description', 'project', 'admin']
