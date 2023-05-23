from tools.generic_urls import add_url_from_generic_views

app_name = 'projects'
urlpatterns = add_url_from_generic_views('projects.views')
