from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from tools.generic_class import GenericClass


class ProjectCategory(GenericClass):
    refer_team = models.ForeignKey('teams.Team', verbose_name=_("Team"), on_delete=models.CASCADE, null=True,
                                   blank=True)
    refer_project = models.ForeignKey('projects.Project', verbose_name=_("Project"), on_delete=models.CASCADE)
    refer_category = models.ForeignKey('categories.Category', verbose_name=_("Category"), on_delete=models.CASCADE)
    members = models.ManyToManyField('customusers.CustomUser', verbose_name=_("Members"), blank=True)
    deprecated = models.BooleanField(default=False)

    def get_team(self):
        return self.refer_team

    def save(self, *args, **kwargs):
        creation = 0
        if self._state.adding:
            creation = 1
        if not self.refer_team:
            self.refer_team = self.get_team()
        super(ProjectCategory, self).save(*args, **kwargs)
        if self.refer_project:
            if self not in self.refer_project.project_categories.all():
                self.refer_project.project_categories.add(self)
        if creation:
            self.refer_project.categories.add(self.refer_category)

    class Meta:
        verbose_name = _('category for project')
        verbose_name_plural = _('categories for projects')
        ordering = ('pk',)

    def __str__(self):
        return "%s - %s - %s" % (
            self.refer_team if self.refer_team else "None", self.refer_project, self.refer_category)


@receiver(m2m_changed, sender=ProjectCategory.members.through)
def projectcategories_members_changed(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        for pk in kwargs["pk_set"]:
            if len(instance.members.all()):
                users = instance.members.filter(pk=pk)
                if len(users):
                    user = users[0]
                    if instance not in user.categories.all():
                        user.categories.add(instance)

    elif action == "pre_remove":
        for pk in kwargs["pk_set"]:
            if len(instance.members.all()):
                users = instance.members.filter(pk=pk)
                if len(users):
                    user = users[0]
                    if instance in user.categories.all():
                        user.categories.remove(instance)
