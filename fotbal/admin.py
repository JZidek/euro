from django.contrib import admin
from .models import Zapasy_fotbal, Tipy_fotbal,Tymy_fotbal, Komenty
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField


admin.site.register(Zapasy_fotbal)
admin.site.register(Tipy_fotbal)
admin.site.register(Tymy_fotbal)
admin.site.register(Komenty)