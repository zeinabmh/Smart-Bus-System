from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('homepage', views.homepage, name="homepage"),
    path('reservations', views.reservations, name="reservations"),
    path('payments', views.payments, name="payments"),
    path('sendnot', views.sendnot, name="sendnot"),
    path('resetpassword', views.resetpassword, name="resetpassword"),
    path('forgetpass', views.forgetpass, name="forgetpass"),
    path('payments', views.payments, name="payments"),
    path('sendnot', views.sendnot, name="sendnot"),
    path('send_not/', views.send_not, name="send_not"),
   
    
    
    ]