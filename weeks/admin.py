from django.contrib import admin
from .models import Week, WeekDate


# Register your models here.
class WeekAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    filter_horizontal = ('days',)


class WeekDateAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Week, WeekAdmin)
admin.site.register(WeekDate, WeekDateAdmin)
