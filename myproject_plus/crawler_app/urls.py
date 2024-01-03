from django.urls import path, re_path
from . import views

urlpatterns = [
    path('xitong_li/<int:page>/', views.update_pie_chart, name='update_pie_chart'),
    path('detail_page/', views.detail_page, name='detail_page'),
]
