import os
from calendar import monthrange
from datetime import date

import xlsxwriter
from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from tools.generic_class import GenericClass


class UserMonthlyReport(GenericClass):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, )
    year = models.PositiveIntegerField(default=2023)
    month = models.PositiveIntegerField(default=1)
    days = models.ManyToManyField("days.Day", verbose_name=_('days'), blank=True)
    refer_mr = models.ForeignKey("reports.MonthlyReport", on_delete=models.CASCADE, null=True, blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return "%s/%02d %s" % (self.year, self.month, self.user.get_full_name())

    def get_detail_url(self):
        self.detail_url = '%s:umr_detail' % self.app_name
        return reverse(self.detail_url, kwargs={'mr_pk': self.refer_mr.pk, 'pk': self.pk})

    def get_xls_url(self):
        return reverse('%s:umr_xls' % self.app_name, kwargs={'mr_pk': self.refer_mr.pk, 'pk': self.pk})

    def get_pdf_url(self):
        return reverse('%s:umr_pdf' % self.app_name, kwargs={'mr_pk': self.refer_mr.pk, 'pk': self.pk})

    def is_completed(self):
        return self.get_planned_hours() == self.get_encoded_hours()

    def get_planned_hours(self):
        sum = 0
        last_day = monthrange(self.year, self.month)[1]
        for i in range(last_day):
            if date(self.year, self.month, i + 1).isoweekday() not in [6, 7]:
                sum += 1
        return (sum - self.refer_mr.get_count_holidays()) * settings.MAX_HOURS_DAY

    def get_encoded_hours(self):
        sum = 0
        for d in self.days.filter(type="default"):
            sum += d.get_sum_day()
        return sum if sum % 1 else int(sum)

    def generate_umr_sheet(self, workbook):
        worksheet = workbook.add_worksheet(self.user.get_folder_name())
        worksheet.write('A1', "%s %s" % (self.user.first_name, self.user.last_name))
        worksheet.write('A2', "%s / %s" % (self.month, self.year))
        line = 5
        for day in self.days.all().order_by('day'):
            for slot in day.slots.all():
                if slot.duration:
                    worksheet.write('A%s' % line, str(slot.refer_day.day))
                    worksheet.write('B%s' % line, str(slot.refer_category.refer_project.name))
                    worksheet.write('C%s' % line, str(slot.refer_category.refer_category.name))
                    worksheet.write('D%s' % line, str(slot.duration))
                    line += 1
        return workbook

    def generate_umr(self):
        filename = "%s%02d_timesheets_report_%s.xlsx" % (self.year, self.month, self.user.get_folder_name())
        path = os.path.join(self.user.get_path_report_folder(self.month, self.year), filename)
        if os.path.exists(path):
            os.remove(path)
        workbook = xlsxwriter.Workbook(path)
        workbook = self.generate_umr_sheet(workbook)
        workbook.close()
        return path, filename

    class Meta:
        verbose_name = _('user monthly report')
        verbose_name_plural = _('user monthly reports')
        ordering = ('pk',)


class MonthlyReport(GenericClass):
    year = models.PositiveIntegerField(default=2023)
    month = models.PositiveIntegerField(default=1)
    holidays = models.ManyToManyField("holidays.Holiday", verbose_name=_('holidays'), blank=True)
    umrs = models.ManyToManyField(UserMonthlyReport, verbose_name=_('UserMonthlyReports'), blank=True)
    team = models.ForeignKey("teams.Team", on_delete=models.CASCADE, null=True, blank=True)
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return "%s/%02d" % (self.year, self.month)

    def get_umrs_list(self):
        l = self.umrs.all().order_by('year', '-month')
        return l

    def get_xls_url(self):
        return reverse('%s:mr_xls' % self.app_name, kwargs={'pk': self.pk})

    def get_zip_url(self):
        return reverse('%s:mr_zip' % self.app_name, kwargs={'pk': self.pk})

    def get_count_holidays(self):
        return len(self.holidays.all())

    def is_completed(self):
        completed = True
        for umr in self.umrs.all():
            if completed:
                completed = (umr.get_planned_hours() == umr.get_encoded_hours())
        return completed

    def get_path_report_folder(self):
        def create_if_not_exists(path):
            if not os.path.exists(path):
                os.makedirs(path)

        path = os.path.join(settings.MEDIA_ROOT, settings.REPORT_FOLDER)
        create_if_not_exists(path)
        path = os.path.join(path, "All")
        create_if_not_exists(path)
        path = os.path.join(path, str(self.year))
        create_if_not_exists(path)
        path = os.path.join(path, "%02d" % self.month)
        create_if_not_exists(path)
        return path

    def generate_mr(self):
        filename = "%s%02d_timesheets_report_all.xlsx" % (self.year, self.month)
        path = os.path.join(self.get_path_report_folder(), filename)
        if os.path.exists(path):
            os.remove(path)
        workbook = xlsxwriter.Workbook(path)
        for umr in self.umrs.all():
            workbook = umr.generate_umr_sheet(workbook)
        workbook.close()
        return path, filename

    class Meta:
        verbose_name = _('monthly report')
        verbose_name_plural = _('monthly reports')
        ordering = ('year', 'month')
