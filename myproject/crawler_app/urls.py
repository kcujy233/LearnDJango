from django.urls import path
from . import views

urlpatterns = [
    path('xitong_li/', views.update_pie_chart, name='update_pie_chart'),
]
