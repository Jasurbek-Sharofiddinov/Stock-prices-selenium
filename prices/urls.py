from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='interface'),
    path('download-excel/', views.download_prices_excel, name='download_excel'),
]
