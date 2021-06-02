from django.contrib import admin
from .models import Zapasy, Tipy
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


admin.site.register(Zapasy)
admin.site.register(Tipy)