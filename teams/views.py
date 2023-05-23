from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tools.generic_views import *
from .forms import CreateTeamForm, TeamForm
from .models import Team


class TeamCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = Team
    fields = None
    form_class = CreateTeamForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new team created.'
    success_url = reverse_lazy('day:team_list')


class TeamListView(LoginRequiredMixin, GenericListView):
    model = Team
    template_name = 'teams_list.html'

    def get_queryset(self):
        return Team.objects.all().order_by('name')


class TeamUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Team
    fields = None
    form_class = TeamForm

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class TeamDetailView(LoginRequiredMixin, GenericDetailView):
    model = Team
    template_name = 'teams_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().get_teamleaders())
        return super().dispatch(request, *args, **kwargs)


class TeamDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Team
