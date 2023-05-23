from django.contrib import admin
from .models import Project


# Register your models here.
class ProjectAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    filter_horizontal = ['categories', 'project_categories']


admin.site.register(Project, ProjectAdmin)
