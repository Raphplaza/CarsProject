from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from carapp import views

urlpatterns = [
    path('cars/', views.car_list),
    path('cars/<int:pk>/', views.car_detail),
    path('popular', views.car_list_popular),
    path('rates/<int:pk>/', views.rate_list),
    path('rate', views.rate),
]

urlpatterns = format_suffix_patterns(urlpatterns)