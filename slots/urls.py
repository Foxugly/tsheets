from django.urls import path

from tools.generic_urls import add_url_from_generic_views
from .views import slot_ajax_update

app_name = 'slots'
urlpatterns = add_url_from_generic_views('slots.views')
urlpatterns += [
    path('ajax/update/', slot_ajax_update, name='slots_ajax_update'),

]
