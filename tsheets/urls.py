import json

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import path, include, reverse
from django.utils import translation
from django.utils.translation import check_for_language

from customusers.views import SettingsUpdateView
from holidays.cron import update_days_from_holiday
from teams.models import Team
from tools.generic_views import is_ajax


@login_required
def home(request):
    update_days_from_holiday()
    return redirect("week:week_list")


def set_lang(request):
    response = None
    if 'lang' in request.GET and check_for_language(request.GET.get('lang')):
        user_language = request.GET.get('lang')
        translation.activate(user_language)
        if 'next' in request.GET:
            response = HttpResponseRedirect(request.GET.get('next'))
        else:
            response = HttpResponseRedirect(reverse('home'))
        response.set_cookie(
            settings.LANGUAGE_COOKIE_NAME,
            user_language,
            max_age=settings.LANGUAGE_COOKIE_AGE,
            path=settings.LANGUAGE_COOKIE_PATH,
            domain=settings.LANGUAGE_COOKIE_DOMAIN,
            secure=settings.LANGUAGE_COOKIE_SECURE,
            httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
            samesite=settings.LANGUAGE_COOKIE_SAMESITE,
        )
    return response


@login_required
def set_team(request):
    results = {}
    if is_ajax(request):
        if 'team' in request.POST:
            t = get_object_or_404(Team, slug=request.POST['team'])
            request.user.current_team = t
            request.user.save()
            results['return'] = True
        else:
            results['return'] = False
    else:
        results['return'] = False
    return HttpResponse(json.dumps(results))


urlpatterns = [
    path('', home, name='home'),
    path('team/', include('teams.urls', namespace='team')),
    path('project/', include('projects.urls', namespace='project')),
    path('projectcategory/', include('projectcategories.urls', namespace='projectcategory')),
    path('category/', include('categories.urls', namespace='category')),
    path('week/', include('weeks.urls', namespace='week')),
    path('day/', include('days.urls', namespace='day')),
    path('holiday/', include('holidays.urls', namespace='holiday')),
    path('slot/', include('slots.urls', namespace='slot')),
    path('user/', include('customusers.urls', namespace='customuser')),
    path('report/', include('reports.urls', namespace='report')),
    path('lang/', set_lang, name='lang'),
    path('hijack/', include('hijack.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/settings/', SettingsUpdateView.as_view(), name='settings'),
    path('accounts/ajax/team/', set_team, name='ajax_team'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls))]

if not settings.DEBUG:
    handler400 = 'tsheets.urls.bad_request'
    handler403 = 'tsheets.urls.permission_denied'
    handler404 = 'tsheets.urls.page_not_found'
    handler500 = 'tsheets.urls.server_error'


def bad_request(request, exception):
    context = {}
    return render(request, '400.html', context, status=400)


def permission_denied(request, exception):
    context = {}
    return render(request, '403.html', context, status=403)


def page_not_found(request, exception):
    context = {}
    return render(request, '404.html', context, status=404)


def server_error(request):
    context = {}
    return render(request, '500.html', context, status=500)
