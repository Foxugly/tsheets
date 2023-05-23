from django.contrib import admin
from .models import Holiday


class HolidayAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)


admin.site.register(Holiday, HolidayAdmin)
