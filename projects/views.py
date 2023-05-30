from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from projects.forms import ProjectForm, CreateProjectForm
from projects.models import Project
from tools.generic_views import *


class ProjectCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = Project
    fields = None
    form_class = CreateProjectForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new project created.'
    success_url = reverse_lazy('project:project_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

    def form_valid(self, form):
        form.instance.team = self.request.user.current_team
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        else:
            return self.success_url


class ProjectListView(LoginRequiredMixin, GenericListView):
    model = Project
    template_name = 'projects_list.html'

    def get_queryset(self):
        return Project.objects.all().order_by(
            'name') if self.request.user.is_superuser else self.request.user.current_team.projects.all().order_by(
            'name')

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.current_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Project
    fields = None
    form_class = ProjectForm

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectDetailView(LoginRequiredMixin, GenericDetailView):
    model = Project
    template_name = 'projects_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class ProjectDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = Project
    template_name = 'generic_delete.html'
    success_url = reverse_lazy('project:project_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.deprecated = True
        return HttpResponseRedirect(success_url)

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)
