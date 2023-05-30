from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from tools.generic_class import GenericClass
from weeks.models import WeekDate


# Create your models here.
class Team(GenericClass):
    name = models.CharField(max_length=50, verbose_name=_("name"), )
    slug = models.SlugField(max_length=50, null=True, blank=True)
    teamleaders = models.ManyToManyField('customusers.CustomUser', verbose_name=_('teamleaders'),
                                         related_name="teamleaders", blank=True)
    members = models.ManyToManyField('customusers.CustomUser', verbose_name=_('member'), related_name="member",
                                     blank=True)
    deprecated = models.BooleanField(default=False)
    projects = models.ManyToManyField('projects.Project', verbose_name=_('projects'), related_name="projects",
                                      blank=True)

    def get_teamleaders(self):
        return list(self.teamleaders.all().order_by("last_name"))

    def get_members(self):
        return list(self.members.all().order_by("last_name"))

    def get_projects(self):
        return list(self.projects.all().order_by("name"))

    def get_all_members(self):
        return list(set(self.teamleaders.all()) | set(self.members.all()))

    def is_teamleader(self, user):
        return user in self.teamleaders.all()

    def is_member(self, user):
        return user in self.members.all()

    def get_weeks(self):
        return list(WeekDate.objects.all())

    def get_role(self, user):
        if self.is_teamleader(user):
            return "teamleader"
        elif self.is_member(user):
            return "member"
        else:
            return None

    def __str__(self):
        return "%s" % (self.name)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = _('Team')
        verbose_name_plural = _('Teams')
        ordering = ('name',)


@receiver(m2m_changed, sender=Team.projects.through)
def team_projects_changed(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        for pk in kwargs["pk_set"]:
            if instance.projects.all().exists():
                projects = instance.projects.filter(pk=pk)
                if projects.exists():
                    project = projects[0]
                    project.refer_team = instance
                    project.save()
    elif action == "pre_remove":
        for pk in kwargs["pk_set"]:
            if instance.projects.all().exists():
                projects = instance.projects.filter(pk=pk)
                if projects.exists():
                    project = projects[0]
                    project.refer_team = None
                    project.save()
