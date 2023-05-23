from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from days.models import Day
from reports.models import MonthlyReport
from tools.generic_class import GenericClass


class Holiday(GenericClass):
    day = models.DateField(_("Date"), default=datetime.now)

    class Meta:
        verbose_name = _('holiday')
        verbose_name_plural = _('holidays')
        ordering = ('pk',)

    def __str__(self):
        return "%s" % self.day.strftime("%d/%m/%Y")

    def save(self, *args, **kwargs):
        creation = 0
        if self._state.adding:
            creation = 1
        super().save(*args, **kwargs)
        if creation:
            mr, created = MonthlyReport.objects.get_or_create(year=self.day.year, month=self.day.month, team=self.team)
            if created:
                mr.save()
            mr.holidays.add(self)
            for day in Day.objects.filter(day=self.day):
                day.type = day.TYPE_CHOICES[2][0]
                day.save()
                for slot in day.slots.all():
                    slot.duration = 0
                    slot.save()
