from django.contrib import admin
from .models import Team


# Register your models here.
class TeamAdmin(admin.ModelAdmin):

    filter_horizontal = ['teamleaders', 'members', 'projects']


admin.site.register(Team, TeamAdmin)
