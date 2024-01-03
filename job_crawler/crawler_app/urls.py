# crawler_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('update-pie-chart/', views.update_pie_chart, name='update_pie_chart'),
]
