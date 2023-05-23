from tools.generic_class import GenericClass
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from datetime import timedelta, datetime


class Category(GenericClass):
    name = models.CharField(max_length=100, verbose_name=_("name"), blank=True, null=True)
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("description"), )
    to_projects = models.BooleanField(default=False)
    to_admin = models.BooleanField(default=False)
    deprecated = models.BooleanField(default=False)

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ('name',)
