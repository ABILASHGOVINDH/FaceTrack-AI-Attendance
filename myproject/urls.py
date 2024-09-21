from django.contrib import admin
from django.urls import path
from calc import views 

urlpatterns = [
    path('', views.home),
    # path('login/', views.login),
    # path('take_images/', views.take_images, name='take_images')
   
]
