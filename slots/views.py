import json

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.translation import gettext as _

from tools.generic_views import is_ajax
from .models import Slot


@login_required
def slot_ajax_update(request):
    results = {}
    if is_ajax(request): #TODO check access
        s = Slot.objects.get(id=request.POST['id'])
        s.duration = request.POST['duration'] if request.POST['duration'] else 0
        s.save()
        sum_day = s.refer_day.get_sum_day()
        results['sum_weekday'] = str(sum_day)
        if sum_day < 0:
            results['return'] = False
            results['toast_title'] = _("Duration alert")
            results['toast_content'] = _(
                "The encoded duration cannot be negative.")
        elif sum_day > request.user.hours_max:
            results['return'] = False
            results['toast_title'] = _("Duration alert")
            results['toast_content'] = _(
                "The encoded duration for the day is more than %d hours." % settings.MAX_HOURS_DAY)
        else:
            results['return'] = True
        results['weekday'] = str(s.refer_day.day.weekday())
        results['sum_weekday'] = str(s.refer_day.get_sum_day())
    else:
        results['return'] = False
        results['toast_title'] = _("Connexion")
        results['toast_content'] = _("unauthorised access")
    return HttpResponse(json.dumps(results))
