from bootstrap_modal_forms.forms import BSModalModelForm
from django.forms import ModelForm, Textarea, CharField

from .models import Category


class CategoryForm(ModelForm):
    model = Category
    description = CharField(widget=Textarea(), required=False)

    class Meta:
        model = Category
        fields = '__all__'


class CreateCategoryForm(BSModalModelForm):
    model = Category
    description = CharField(widget=Textarea(), required=False)

    class Meta:
        model = Category
        fields = ['name', 'description', 'to_projects']
