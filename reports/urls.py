from django.urls import path

from tools.generic_urls import add_url_from_generic_views
from .views import UserMonthlyReportDetailView, generate_xls_umr, generate_pdf_umr, generate_xls_mr, generate_zip_mr



app_name = 'reports'
urlpatterns = add_url_from_generic_views('reports.views')
urlpatterns += [
    path('<int:mr_pk>/umr/<int:pk>/', UserMonthlyReportDetailView.as_view(), name='umr_detail'),
    path('<int:mr_pk>/umr/<int:pk>/xls/', generate_xls_umr, name='umr_xls'),
    path('<int:mr_pk>/umr/<int:pk>/pdf/', generate_pdf_umr, name='umr_pdf'),
    path('<int:pk>/xls/', generate_xls_mr, name='mr_xls'),
    path('<int:pk>/zip/', generate_zip_mr, name='mr_zip'),
]
