from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm, Textarea, CharField

from .models import ProjectCategory


class ProjectCategoryForm(ModelForm):
    model = ProjectCategory

    class Meta:
        model = ProjectCategory
        fields = ['refer_team', 'refer_project', 'refer_category', 'members', 'deprecated']


class CreateProjectCategoryForm(BSModalModelForm):
    model = ProjectCategory
    description = CharField(widget=Textarea(), required=False)

    class Meta:
        model = ProjectCategory
        fields = ['refer_project', 'refer_category']
