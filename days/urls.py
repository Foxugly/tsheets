from tools.generic_urls import add_url_from_generic_views
from django.urls import path

app_name = 'days'
urlpatterns = add_url_from_generic_views('days.views')

