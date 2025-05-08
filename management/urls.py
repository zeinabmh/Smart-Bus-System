from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index, name="index"),
    path('options', views.options, name='options'),
    path('adddriver', views.adddriver, name='adddriver'),
    path('deletedriver', views.deletedriver, name='deletedriver'),
    path('showdriver', views.showdriver, name='showdriver'),
]
