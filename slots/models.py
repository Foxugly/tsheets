from django.db import models
from django.utils.translation import gettext_lazy as _

from tools.generic_class import GenericClass


class Slot(GenericClass):
    refer_category = models.ForeignKey('projectcategories.ProjectCategory', verbose_name=_('category'),
                                       related_name="back_slot_projectcategory",
                                       null=True, on_delete=models.CASCADE, )
    refer_day = models.ForeignKey('days.Day', verbose_name=_('Day'), related_name="back_slot_day",
                                  null=True, on_delete=models.CASCADE, )
    refer_user = models.ForeignKey('customusers.CustomUser', verbose_name=_('user'), related_name="back_slot_user",
                                   null=True, on_delete=models.CASCADE, )
    duration = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    lock = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.refer_day.update_sum_day()

    def as_json(self, **kwargs):
        duration = ""
        if self.duration and self.duration > 0:
            duration = self.duration if self.duration % 1 else int(self.duration)
        d = {'id': str(self.id), 'can_edit': True, 'duration': duration, 'type': self.refer_day.type}
        return d

    class Meta:
        verbose_name = _('slot')
        verbose_name_plural = _('slots')
        ordering = ('pk',)

    def __str__(self):
        return "[%s][%s] %s" % (self.refer_day.day, self.refer_user, self.refer_category)
