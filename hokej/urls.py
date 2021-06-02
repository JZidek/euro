from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views, url_handlers

urlpatterns = [
    path('hokej/zapasy_skupina', views.login, name="zapasy_skupina"),
    #path('hokej/poradi', views.login, name="poradi")
    #path('logo', views.pg2, name="logo"),
    #path("upload/", views.Upload.as_view()),
    path('', url_handlers.index_handler),
]
