from django.urls import path
from . import views

urlpatterns = [
    path('', views.redirect_to_svdogsitters),
    path('svdogsitters', views.show_svdogsitters),
    path('svdogsitters/registration', views.show_registration_form),
    path('svdogsitters/register', views.register),
    path('svdogsitters/login', views.login),
    path('svdogsitters/logout', views.logout),
    path('svdogsitters/pet_registration', views.show_pet_registration_form),
    path('svdogsitters/pet_register', views.pet_register),
    path('svdogsitters/welcome', views.show_welcome),
    path('svdogsitters/request', views.request)
]