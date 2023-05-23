from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from categories.models import Category
from tools.generic_views import *
from .forms import CreateCategoryForm, CategoryForm


class CategoryCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = Category
    fields = None
    form_class = CreateCategoryForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new category created.'
    success_url = reverse_lazy('category:category_list')


class CategoryListView(LoginRequiredMixin, GenericListView):
    model = Category
    template_name = 'categories_list.html'

    def get_queryset(self):
        return Category.objects.filter().order_by('name')


class CategoryUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Category
    fields = None
    form_class = CategoryForm


class CategoryDetailView(LoginRequiredMixin, GenericDetailView):
    model = Category
    template_name = 'categories_detail.html'


class CategoryDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Category

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deprecated = True
        self.object.save()
        return HttpResponseRedirect(success_url)

