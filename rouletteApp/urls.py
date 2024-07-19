from django.urls import path
from . import views

urlpatterns = [
    path('process_receipt/', views.process_receipt, name='process_receipt'),
    path('get_points/<str:id>/', views.get_points, name='get_points'),
]
