from datetime import timedelta

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from days.models import Day
from holidays.models import Holiday
from slots.models import Slot
from tools.generic_class import GenericClass


class WeekDate(GenericClass):
    year = models.PositiveIntegerField(default=2023)
    week = models.PositiveIntegerField(default=20)
    start_date = models.DateField(null=True, blank=True, verbose_name=_("start date"), )
    end_date = models.DateField(null=True, blank=True, verbose_name=_("end date"), )
    days_max = models.PositiveIntegerField(default=5)

    def refresh_days_max(self):
        hs = Holiday.objects.filter(day__range=(self.start_date, self.end_date))
        self.days_max = 5 - len(hs)
        self.save()

    def __str__(self):
        return "%s/W%s : %s - %s" % (
            self.year, self.week, self.start_date.strftime("%d/%m/%Y"), self.end_date.strftime("%d/%m/%Y"))

    class Meta:
        verbose_name = _('weekdate')
        verbose_name_plural = _('weekdates')
        ordering = ('-start_date',)


class Week(GenericClass):
    weekdate = models.ForeignKey(WeekDate, verbose_name=_('week'), related_name="weekdate", null=True,
                                 on_delete=models.CASCADE, )
    days = models.ManyToManyField(Day, blank=True, verbose_name=_("days"), )
    refer_user = models.ForeignKey('customusers.CustomUser', verbose_name=_('user'), related_name="back_week_user",
                                   null=True, on_delete=models.CASCADE, )
    refer_team = models.ForeignKey('teams.Team', verbose_name=_('team'), related_name="week_refer_team",
                                   null=True, on_delete=models.CASCADE, )
    days_max = models.PositiveIntegerField(default=5)
    lock = models.BooleanField(default=False)
    deprecated = models.BooleanField(default=False)

    def get_range_max_available_days(self):
        return range(0, len(self.days.filter(type=Day.TYPE_CHOICES[0][0])) + 1)

    def get_next_week(self):
        first_day_next_week = self.weekdate.start_date + timedelta(days=7)
        next_week = first_day_next_week.isocalendar().week
        next_year = first_day_next_week.isocalendar().year
        wd, created = WeekDate.objects.get_or_create(week=next_week, year=next_year, start_date=first_day_next_week,
                                                     end_date=first_day_next_week + timedelta(days=6))
        if created:
            wd.refresh_days_max()
        w, created = Week.objects.get_or_create(weekdate=wd, refer_user=self.refer_user)
        if created:
            w.days_max = min(self.days_max, self.refer_user.days_max)
            w.save()
        return w

    def has_next_week(self):
        first_day_next_week = self.weekdate.start_date + timedelta(days=7)
        next_week = first_day_next_week.isocalendar().week
        next_year = first_day_next_week.isocalendar().year
        wd = WeekDate.objects.filter(week=next_week, year=next_year, start_date=first_day_next_week,
                                     end_date=first_day_next_week + timedelta(days=6))
        if len(wd):
            w = Week.objects.filter(weekdate=wd[0], refer_user=self.refer_user)
            return True if len(w) else False
        else:
            return False

    def get_previous_week(self):
        first_day_last_week = self.weekdate.start_date - timedelta(days=7)
        prev_week = first_day_last_week.isocalendar().week
        prev_year = first_day_last_week.isocalendar().year
        wd, created = WeekDate.objects.get_or_create(week=prev_week, year=prev_year, start_date=first_day_last_week,
                                                     end_date=first_day_last_week + timedelta(days=6))
        if created:
            wd.refresh_days_max()
        w, created = Week.objects.get_or_create(weekdate=wd, refer_user=self.refer_user, )
        if created:
            w.days_max = min(self.days_max, self.refer_user.days_max)
            w.save()
        return w

    def has_previous_week(self):
        first_day_prev_week = self.weekdate.start_date - timedelta(days=7)
        prev_week = first_day_prev_week.isocalendar().week
        prev_year = first_day_prev_week.isocalendar().year
        wd = WeekDate.objects.filter(week=prev_week, year=prev_year, start_date=first_day_prev_week,
                                     end_date=first_day_prev_week + timedelta(days=6))
        if len(wd):
            w = Week.objects.filter(weekdate=wd[0], refer_user=self.refer_user)
            return True if len(w) else False
        else:
            return False

    def get_sum_days(self):
        sum_days = []
        for day in self.days.all().order_by("day__day").order_by("day"):
            sum_days.append({"type": day.type, "sum": day.get_sum_day(), "weekday": day.day.weekday()})
        return sum_days

    def get_sum_week(self):
        sum_days = 0
        for day in self.days.all().order_by("day__day"):
            sum_days += day.get_sum_day()
        return sum_days if sum_days % 1 else int(sum_days)

    def get_sum_max_week(self):
        sum_days = 0
        for day in self.days.all().order_by("day__day"):
            if day.type == Day.TYPE_CHOICES[0][0]:
                sum_days += settings.MAX_HOURS_DAY
        return sum_days if sum_days % 1 else int(sum_days)

    def is_completed(self):
        return -1 if self.get_sum_week() == 0 else 1 if self.get_sum_max_week() == self.get_sum_week() else 0

    def get_days(self):
        days = []
        for i in range(7):
            d = self.weekdate.start_date + timedelta(days=i)
            date_label = d.strftime('%a %d/%m/%y')
            h = Holiday.objects.filter(day=d)
            if i >= 5:
                days.append({'date': date_label, 'type': "weekend"})
            elif len(h):
                days.append({'date': date_label, 'type': "holiday"})
            else:
                days.append({'date': date_label, 'type': "default"})
        return days

    def get_projects(self):
        projects = set()
        for d in self.days.all():
            for s in d.slots.all():
                projects.add(s.refer_category.refer_project)
        return sorted(projects, key=lambda x: x.name)

    def get_categories(self, project):
        categories = set()
        for d in self.days.all():
            for s in d.slots.all():
                if s.refer_category.refer_project == project:
                    if s.refer_category in s.refer_user.categories.filter(deprecated=False):
                        categories.add(s.refer_category.refer_category)
        return sorted(categories, key=lambda x: x.name)

    def get_projects_categories_days_slots(self):
        projects = []
        for p in self.get_projects():
            cats = []
            for c in self.get_categories(p):
                slots = []
                for d in range(5):
                    day = self.weekdate.start_date + timedelta(days=d)
                    s = []
                    if not Holiday.objects.filter(day=day):
                        s = Slot.objects.filter(refer_user=self.refer_user, refer_category__refer_category=c,
                                                refer_category__refer_project=p, refer_day__day=day)
                    if len(s):
                        slots.append(s[0].as_json())
                    else:
                        # slots.append({'type': "weekend"})
                        slots.append({'type': Day.TYPE_CHOICES[2][0]})  # holiday
                cats.append({'name': c.name, 'slots': slots})
            projects.append({'name': p, 'categories': cats})
        return projects

    def save(self, *args, **kwargs):
        creation = 0
        if self._state.adding:
            creation = 1
        super().save(*args, **kwargs)
        if creation:
            self.reload_slots()

    def reload_slots(self):
        if self.refer_user:
            if self not in self.refer_user.weeks.all():
                self.refer_user.weeks.add(self)
        for i in range(5):
            d, created = Day.objects.get_or_create(day=self.weekdate.start_date + timedelta(days=i), refer_week=self,
                                                   refer_user=self.refer_user)
            if created:
                if len(Holiday.objects.filter(day=d.day)):
                    d.type = Day.TYPE_CHOICES[2][0]  # holiday
                d.save()
            if d not in self.days.all():
                self.days.add(d)
            for pc in self.refer_user.categories.filter(deprecated=False):
                s, created = Slot.objects.get_or_create(refer_user=self.refer_user, refer_category=pc, refer_day=d)
                if created:
                    s.save()
                if s not in d.slots.all():
                    d.slots.add(s)

    def __str__(self):
        return "%s %s" % (self.refer_user.get_full_name(), self.weekdate)

    class Meta:
        verbose_name = _('week')
        verbose_name_plural = _('weeks')
        ordering = ('pk',)
