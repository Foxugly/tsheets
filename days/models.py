from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _

from reports.models import UserMonthlyReport, MonthlyReport
from slots.models import Slot
from tools.generic_class import GenericClass


class Day(GenericClass):
    TYPE_CHOICES = (
        ('default', _('default')),
        ('weekend', _('weekend')),
        ('holiday', _('holiday')),
    )

    day = models.DateField(_("Date"), default=datetime.now)
    slots = models.ManyToManyField(Slot, blank=True, verbose_name=_("slots"), )
    refer_week = models.ForeignKey('weeks.Week', verbose_name=_('Week'), related_name="back_day_week",
                                   null=True, on_delete=models.CASCADE, )
    refer_user = models.ForeignKey('customusers.CustomUser', verbose_name=_('user'), related_name="back_day_user",
                                   null=True, on_delete=models.CASCADE, )
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0])
    sum_day = models.PositiveIntegerField(default=0)

    def update_sum_day(self):
        sum = 0
        if self.type == self.TYPE_CHOICES[0][0]:
            for ds in self.slots.all():
                sum += ds.duration if ds.duration else 0
        if int(sum) != self.sum_day:
            self.sum_day = int(sum)
            self.save()
            self.refer_week.update_sum_week()

    def clean_slots(self):
        for s in self.slots.all():
            s.duration = 0
            s.save()
        self.sum_day = 0
        self.save()
        self.refer_week.update_sum_week()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        mr = None
        umr, umr_created = UserMonthlyReport.objects.get_or_create(user=self.refer_user, year=self.day.year,
                                                                   month=self.day.month,
                                                                   team=self.refer_week.refer_team)
        if umr_created:
            umr.save()
            mr, mr_created = MonthlyReport.objects.get_or_create(year=self.day.year, month=self.day.month,
                                                                 team=self.refer_week.refer_team)
            if mr_created:
                mr.save()
            mr.umrs.add(umr)
            umr.refer_mr = mr
            umr.save()
        umr.days.add(self)

    class Meta:
        verbose_name = _('day')
        verbose_name_plural = _('days')
        ordering = ('pk',)

    def __str__(self):
        return "[%s] %s" % (self.refer_user, self.day)
