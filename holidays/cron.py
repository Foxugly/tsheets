from holidays.models import Holiday
from days.models import Day


def update_days_from_holiday():
    for h in Holiday.objects.filter(done=False):
        if h.to_delete:
            type_id = 1 if h.day.isoweekday() in [6, 7] else 0
            for day in Day.objects.filter(day=h.day):
                day.type = day.TYPE_CHOICES[type_id][0]
                day.save()
                day.refer_week.update_sum_week()
            h.delete()
        else:
            for day in Day.objects.filter(day=h.day):
                day.clean_slots()
                day.type = day.TYPE_CHOICES[2][0]
                day.save()
            h.done = True
            h.save()
