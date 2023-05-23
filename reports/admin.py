from django.contrib import admin

from .models import UserMonthlyReport, MonthlyReport


admin.site.register(UserMonthlyReport)
admin.site.register(MonthlyReport)

