from django.urls import path

from . import views

app_name = 'perfume_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('perfumes_list/',views.perfumes_list,name='perfumes_list'),
    path('perfume/<int:pk>',views.perfume_detail,name='perfume_detail'),

 ]