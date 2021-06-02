from django.contrib import admin 
from django.urls import path 
from django.conf import settings 
from django.conf.urls.static import static 
from . import views, url_handlers

urlpatterns = [
    path('fotbal/zapasy_sk', views.login, name="zapasy_sk"),
    path('', url_handlers.index_handler),
]
