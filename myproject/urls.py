
from django.urls import path
from calc import views 

urlpatterns = [
    path('', views.home),
    path('login/', views.login),
    path('register/', views.register),  # Map the '/register/' URL to the register view
    path('take_images/', views.take_images, name='take_images'),
    path('save profile/', views.save_profile_to_database, name='save profile'),
    path('',views.get_profile_count),
   
]