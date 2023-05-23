from tools.generic_urls import add_url_from_generic_views

app_name = 'categories'
urlpatterns = add_url_from_generic_views('categories.views')
