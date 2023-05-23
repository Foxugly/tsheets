from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from tools.generic_views import *
from .forms import ProjectCategoryForm, CreateProjectCategoryForm
from .models import ProjectCategory


class ProjectCategoryCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = ProjectCategory
    fields = None
    form_class = CreateProjectCategoryForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new project created.'
    success_url = reverse_lazy('project:project_list')

    def form_valid(self, form):
        f = form.save(commit=False)
        f.refer_team = self.request.user.current_team
        f.save()
        return super().form_valid(form)

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        else:
            return self.success_url

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectCategoryListView(LoginRequiredMixin, GenericListView):
    model = ProjectCategory
    template_name = 'projects_categories_list.html'

    def get_queryset(self):
        queryset = None
        if self.request.user.is_superuser:
            queryset = ProjectCategory.objects.filter().order_by('refer_project__name', 'refer_category__name')
        else:
            queryset = ProjectCategory.objects.filter(refer_project__in=self.request.user.get_teamleader_teams())
        return queryset

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.current_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectCategoryUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = ProjectCategory
    fields = None
    form_class = ProjectCategoryForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectCategoryDetailView(LoginRequiredMixin, GenericDetailView):
    model = ProjectCategory
    template_name = 'generic_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectCategoryDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = ProjectCategory

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deprecated = True
        self.object.save()
        return HttpResponseRedirect(success_url)

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders() + [self.get_object().refer_user])
        return super().dispatch(request, *args, **kwargs)
