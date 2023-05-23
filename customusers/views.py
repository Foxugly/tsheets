from bootstrap_modal_forms.generic import BSModalCreateView, BSModalDeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from tools.generic_views import *
from .forms import CustomUserFullForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = CustomUser
    fields = None
    form_class = CustomUserCreationForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new project created.'
    success_url = reverse_lazy('project:project_list')

    def get_success_url(self):
        if "next" in self.request.GET:
            return self.request.GET["next"]
        else:
            return self.success_url

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(request.user.current_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class CustomUserListView(LoginRequiredMixin, GenericListView):
    model = CustomUser
    template_name = 'customuser_list.html'

    def get_queryset(self):
        qs = []
        if self.request.user.is_superuser:
            qs = CustomUser.objects.all().order_by('username')
        elif self.request.user in self.request.user.current_team.get_teamleaders():
            qs = self.request.user.current_team.get_all_members()
        return qs

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.current_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class CustomUserUpdateView(GenericUpdateView):
    model = CustomUser
    fields = None
    form_class = CustomUserFullForm
    template_name = 'generic_update.html'
    success_url = reverse_lazy('settings')
    success_message = _('Changes saved.')

    def __init__(self, *args, **kwargs):
        super(GenericUpdateView, self).__init__(*args, **kwargs)
        self.app_name = "accounts"
        self.model_name = self.model._meta.model_name

    def get_object(self):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['model'] = self.model
        return context

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(request.user.current_team.get_teamleaders(), [self.request.user])
        return super().dispatch(request, *args, **kwargs)


class CustomUserDetailView(LoginRequiredMixin, GenericDetailView):
    model = CustomUser
    template_name = 'projects_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(request.user.current_team.get_teamleaders(), [self.request.user])
        return super().dispatch(request, *args, **kwargs)


class CustomUserDeleteView(LoginRequiredMixin, BSModalDeleteView):
    model = CustomUser
    template_name = 'generic_delete.html'
    success_url = reverse_lazy('project:project_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(request.user.current_team.get_teamleaders())
        return super().dispatch(request, *args, **kwargs)
