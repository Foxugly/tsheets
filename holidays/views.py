from bootstrap_modal_forms.generic import BSModalCreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from tools.generic_views import *
from .forms import CreateHolidayForm, HolidayForm
from .models import Holiday


class HolidayCreateView(LoginRequiredMixin, GenericCreateView, BSModalCreateView):
    model = Holiday
    fields = None
    form_class = CreateHolidayForm
    template_name = 'generic_modal_update.html'
    success_message = 'Success: new holiday created.'
    success_url = reverse_lazy('day:holiday_list')


class HolidayListView(LoginRequiredMixin, GenericListView):
    model = Holiday
    template_name = 'holidays_list.html'

    def dispatch(self, request, *args, **kwargs):
        self.list_access.update([self.request.user])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Holiday.objects.all().order_by('-day')


class HolidayUpdateView(LoginRequiredMixin, GenericUpdateView):
    model = Holiday
    fields = None
    form_class = HolidayForm


class HolidayDetailView(LoginRequiredMixin, GenericDetailView):
    model = Holiday
    template_name = 'holidays_detail.html'


class HolidayDeleteView(LoginRequiredMixin, GenericDeleteView):
    model = Holiday


