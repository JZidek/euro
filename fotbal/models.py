from typing import Iterable
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields.related import ForeignKey


    
class Tymy_fotbal(models.Model):
    skupina = models.CharField(max_length=1)
    tym = models.CharField(max_length=20, unique=True)
    Z = models.IntegerField()
    V = models.IntegerField()
    R = models.IntegerField()
    P = models.IntegerField()
    Gdal = models.IntegerField()
    Gdostal = models.IntegerField()
    skore = models.IntegerField()

    class Meta:
        verbose_name = "tým fotbal"
        verbose_name_plural = "týmy fotbal"
    
    def __str__(self):
        return self.tym
    
class Zapasy_fotbal(models.Model):
    datum = models.DateField()
    cas = models.TimeField()
    skupina = models.CharField(max_length=1)
    tyma = models.CharField(max_length=20)
    tymb = models.CharField(max_length=20)
    scorea = models.IntegerField()
    scoreb = models.IntegerField()
    vysledek = models.IntegerField()

    
    class Meta:
        verbose_name = "zápas fotbal"
        verbose_name_plural = "zápasy fotbal"

    def __str__(self):
        return self.tyma + "-" + self.tymb 


class Tipy_fotbal(models.Model):
    jmeno = models.CharField(max_length=20, unique=True)
    tipy_skore_sk = models.CharField(max_length=250, null=True)
    tipy_skore_v = models.CharField(max_length=32, null=True)

    class Meta:
        verbose_name = "tip fotbal"
        verbose_name_plural = "tipy fotbal"
        
    def __str__(self):
        return self.jmeno

class Komenty(models.Model):
    jmeno = models.CharField(max_length=20)
    koment = models.TextField(max_length=500)
    
    
    class Meta:
        verbose_name = "komentář"
        verbose_name_plural = "komentáře"

    def __str__(self):
        return self.jmeno +": "+self.koment

