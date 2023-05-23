from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from categories.models import Category
from projectcategories.models import ProjectCategory
from teams.models import Team
from tools.generic_class import GenericClass


class Project(GenericClass):
    name = models.CharField(max_length=50, verbose_name=_("name"), )
    description = models.CharField(max_length=300, null=True, blank=True, verbose_name=_("description"), )
    categories = models.ManyToManyField(Category, verbose_name=_('categories'), related_name="categories", blank=True)
    project_categories = models.ManyToManyField(ProjectCategory, verbose_name=_('categories_project'),
                                                related_name="categories_project",
                                                blank=True)
    refer_team = models.ForeignKey('teams.Team', verbose_name=_('team'), related_name="project_refer_team", blank=True,
                                   null=True, on_delete=models.CASCADE, )
    project = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    deprecated = models.BooleanField(default=False)

    def get_team(self):
        return self.refer_team

    def get_list_categories(self):
        return self.project_categories.all().order_by('refer_category__name')

    def save(self, *args, **kwargs):
        creation = False
        if self._state.adding:
            creation = True

        super(Project, self).save(*args, **kwargs)
        if self.deprecated:
            for pc in self.project_categories.all():
                pc.deprecated = True
                pc.save()
        if creation:
            if self.project:
                for cat in Category.objects.filter(to_projects=True):
                    pc = ProjectCategory(refer_category=cat, refer_project=self, refer_team=self.refer_team)
                    pc.save()
                    self.project_categories.add(pc)
            if self.admin:
                for cat in Category.objects.filter(to_admin=True):
                    pc = ProjectCategory(refer_category=cat, refer_project=self, refer_team=self.refer_team)
                    pc.save()
                    self.project_categories.add(pc)
        # check teams
        # TODO adapt if change team
        print(self.project_categories.all())

    def __str__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name = _('projet')
        verbose_name_plural = _('projects')
        ordering = ('name',)


@receiver(m2m_changed, sender=Project.categories.through)
def project_categories_changed(sender, instance, action, *args, **kwargs):
    if action == "post_add":
        for pk in kwargs["pk_set"]:
            cat = Category.objects.get(pk=pk)
            pc, created = ProjectCategory.objects.get_or_create(refer_project=instance, refer_team=instance.refer_team,
                                                                refer_category=cat)
            pc.deprecated = False
            pc.save()
            if pc not in instance.project_categories.all():
                instance.project_categories.add(pc)

    elif action == "post_remove":
        for pk in kwargs["pk_set"]:
            cat = Category.objects.get(pk=pk)
            pc, created = ProjectCategory.objects.get_or_create(refer_project=instance, refer_team=instance.refer_team,
                                                                refer_category=cat)
            pc.deprecated = True
            pc.save()
            if pc in instance.project_categories.all():
                instance.project_categories.remove(pc)
