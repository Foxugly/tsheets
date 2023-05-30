from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from reports.models import MonthlyReport
from tools.generic_class import GenericClass


class Holiday(GenericClass):
    day = models.DateField(_("Date"), default=datetime.now)
    done = models.BooleanField(default=False)
    to_delete = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('holiday')
        verbose_name_plural = _('holidays')
        ordering = ('pk',)

    def __str__(self):
        return "%s" % self.day.strftime("%d/%m/%Y")

    def get_mr(self):
        return MonthlyReport.objects.filter(year=self.day.year, month=self.day.month)
