from django.urls import path
from .views import CompaniesApiView, AreasApiView


urlpatterns = [
    path('', CompaniesApiView.as_view(), name='companies'),
    path('<int:company_id>', CompaniesApiView.as_view(), name='companies'),
    path('areas', AreasApiView.as_view(), name='areas'),
    path('areas/<int:area_id>', AreasApiView.as_view(), name='areas'),
]
