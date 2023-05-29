import os

import unicodedata
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from projectcategories.models import ProjectCategory
from projects.models import Project
from slots.models import Slot
from teams.models import Team
from tools.generic_class import GenericClass
from weeks.models import Week


class CustomUser(AbstractUser, GenericClass):
    language = models.CharField(_("language"), max_length=8, choices=settings.LANGUAGES, default=1)
    hours_max = models.PositiveIntegerField(default=8)
    days_max = models.PositiveIntegerField(default=5)
    weeks = models.ManyToManyField(Week, blank=True)
    categories = models.ManyToManyField(ProjectCategory, blank=True)
    current_team = models.ForeignKey('teams.Team', verbose_name=_("favorite team"), blank=True, null=True,
                                     on_delete=models.CASCADE)

    def get_current_team(self):
        if not self.current_team:
            self.current_team = self.get_teams()[0]
            self.save()
        return self.current_team

    def __str__(self):
        return self.username if not (self.first_name and self.last_name) else self.get_full_name()

    def get_teams(self):
        l = []
        for t in Team.objects.filter(deprecated=False):
            if self in t.get_all_members():
                l.append(t)
        return l

    def get_teamleader_teams(self):
        l = []
        for t in Team.objects.filter(deprecated=False).order_by("name"):
            if t.is_teamleader(self):
                l.append(t)
        return l

    def get_teamleader_project(self):
        l = []
        for t in self.get_teamleader_teams():
            for p in t.projects.all().order_by("name"):
                l.append(p)
        return l

    def get_member_teams(self):
        l = []
        for t in Team.objects.filter(deprecated=False).order_by("name"):
            if t.is_member(self):
                l.append(t)
        return l

    def get_n_teams(self):
        return len(self.get_teams())

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_folder_name(self):
        nfkd_form = unicodedata.normalize('NFKD', self.get_full_name().replace(" ", "_"))
        only_ascii = nfkd_form.encode('ASCII', 'ignore')
        return "%s" % only_ascii.decode('utf-8')

    def get_path_report_folder(self, month, year):
        def create_if_not_exists(path):
            if not os.path.exists(path):
                os.makedirs(path)

        path = os.path.join(settings.MEDIA_ROOT, settings.REPORT_FOLDER)
        create_if_not_exists(path)
        path = os.path.join(path, self.get_folder_name())
        create_if_not_exists(path)
        path = os.path.join(path, str(year))
        create_if_not_exists(path)
        path = os.path.join(path, "%02d" % month)
        create_if_not_exists(path)
        return path


@receiver(m2m_changed, sender=CustomUser.categories.through)
def customuser_categories_changed(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        for pk in kwargs["pk_set"]:
            if len(instance.categories.all()):
                pcs = instance.categories.filter(pk=pk)
                if len(pcs):
                    pc = pcs[0]
                    if instance not in pc.members.all():
                        pc.members.add(instance)

    elif action == "pre_remove":
        for pk in kwargs["pk_set"]:
            if len(instance.categories.all()):
                pcs = instance.categories.filter(pk=pk)
                if len(pcs):
                    pc = pcs[0]
                    if instance in pc.members.all():
                        pc.members.remove(instance)
