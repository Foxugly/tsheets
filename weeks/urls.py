from django.urls import path

from tools.generic_urls import add_url_from_generic_views
from .views import get_next_week, get_previous_week, reload_week, search_week, ajax_update

app_name = 'weeks'
urlpatterns = add_url_from_generic_views('weeks.views')
urlpatterns +=[
    path('<int:pk>/next/', get_next_week, name="week_next"),
    path('<int:pk>/prev/', get_previous_week, name="week_prev"),
    path('<int:pk>/reload/', reload_week, name="week_reload"),
    path('search/', search_week, name="search_reload"),
    path('ajax/update/', ajax_update, name='week_ajax_update'),

]
