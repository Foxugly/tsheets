from django.contrib import admin
from .models import Slot


# Register your models here.
class SlotAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    # filter_horizontal = ('days',)


admin.site.register(Slot, SlotAdmin)
