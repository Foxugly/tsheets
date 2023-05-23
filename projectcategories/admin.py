from django.contrib import admin
from .models import ProjectCategory


# Register your models here.
class ProjectCategoryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    filter_horizontal = ('members',)


admin.site.register(ProjectCategory, ProjectCategoryAdmin)
