import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

from tools.generic_views import *
from .models import MonthlyReport, UserMonthlyReport


# Create your views here.
class ReportListView(LoginRequiredMixin, GenericListView):
    model = MonthlyReport
    template_name = 'reports_list.html'

    #def get_queryset(self):
    #    queryset = self.request.user.projects.all().order_by('id')
    #    return queryset


class ReportDetailView(LoginRequiredMixin, GenericDetailView):
    model = MonthlyReport
    template_name = 'reports_monthly_report_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["umr_title"] = UserMonthlyReport._meta.verbose_name_plural
        return context


class UserMonthlyReportDetailView(LoginRequiredMixin, GenericDetailView):
    model = UserMonthlyReport
    template_name = 'reports_user_monthly_report_detail.html'


def generate_xls_umr(request, mr_pk, pk):
    umr = UserMonthlyReport.objects.get(pk=pk)
    path, filename = umr.generate_umr()
    if os.path.exists(path):
        with open(path, "rb") as file:
            response = HttpResponse(file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


def generate_pdf_umr(request, mr_pk, pk): #TODO
    pass


def generate_xls_mr(request, pk):
    mr = MonthlyReport.objects.get(pk=pk)
    path, filename = mr.generate_mr()
    if os.path.exists(path):
        with open(path, "rb") as file:
            response = HttpResponse(file.read(),
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=%s' % filename
        return response


def generate_zip_mr(request, pk): #TODO
    pass
