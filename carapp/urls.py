from django.urls import path
from carapp import views

urlpatterns = [
    path('cars/', views.car_list),
    path('cars/<int:pk>/', views.car_detail),
]