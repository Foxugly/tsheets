from django.contrib import admin

from .models import Day


class DayAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    filter_horizontal = ('slots',)


admin.site.register(Day, DayAdmin)
