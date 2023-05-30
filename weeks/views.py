import json

from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect

from tools.generic_views import *
from .forms import CreateWeekForm
from .models import Week


class WeekCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = Week
    fields = None
    form_class = CreateWeekForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new week created.'
    success_url = reverse_lazy('week:week_list')

    def form_valid(self, form):
        form.instance.refer_user = self.request.user
        return super().form_valid(form)


class WeekListView(GenericListView):
    model = Week
    template_name = 'weeks_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.current_team.get_teamleaders(), [self.request.user])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.request.user.weeks.filter(refer_team=self.request.user.current_team, deprecated=False).order_by(
            '-weekdate__start_date')
        return queryset


class WeekDetailView(LoginRequiredMixin, GenericDetailView):
    model = Week
    template_name = 'weeks_detail.html'

    def get_context_data(self, **kwargs):
        context = super(WeekDetailView, self).get_context_data(**kwargs)
        return context

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.get_object().refer_team.get_teamleaders(), [self.get_object().refer_user])
        return super().dispatch(request, *args, **kwargs)


class WeekUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Week
    fields = "__all__"  # None

    # form_class = WeekForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # kwargs.update({'user': self.request.user})
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        # teamleaders = self.get_object().refer_team.get_teamleaders() + [self.get_object().refer_user]
        self.list_access.update(self.request.user.current_team.get_teamleaders(), [self.get_object().refer_user])
        return super().dispatch(request, *args, **kwargs)


class WeekDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Week

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update(self.request.user.current_team.get_teamleaders(), [self.get_object().refer_user])
        return super().dispatch(request, *args, **kwargs)


def get_next_week(request, pk):
    current_week = Week.objects.get(pk=pk)
    next_week = current_week.get_next_week()
    return redirect(next_week.get_detail_url())


def get_previous_week(request, pk):
    current_week = Week.objects.get(pk=pk)
    previous_week = current_week.get_previous_week()
    return redirect(previous_week.get_detail_url())


def reload_week(request, pk):
    week = Week.objects.get(pk=pk)
    week.reload_slots()
    return redirect(week.get_detail_url())


@login_required
def search_week(request):
    results = {}
    if is_ajax(request):
        if 'user' in request.POST and len(request.POST['user']) and 'week' in request.POST and len(
                request.POST['week']):
            weeks = Week.objects.filter(refer_user__id=request.POST['user'], weekdate__id=request.POST['week'])
            if len(weeks):
                results['return'] = True
                results['url'] = weeks[0].get_detail_url()
            else:
                results['return'] = False
        else:
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


@login_required
def ajax_update(request):
    results = {'return': True}
    if is_ajax(request):
        w = Week.objects.get(id=request.POST['id'])
        if request.POST['max_day']:
            w.days_max = int(request.POST['max_day'])
            w.save()
        else:
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))
