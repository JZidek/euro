from typing import Iterable
from django.db import models
from django.contrib.auth.models import User


    


class Zapasy(models.Model):
    datum = models.DateField()
    cas = models.TimeField()
    skupina = models.CharField(max_length=1)
    tyma = models.CharField(max_length=20)
    tymb = models.CharField(max_length=20)
    scorea = models.IntegerField()
    scoreb = models.IntegerField()
    vysledek = models.IntegerField()

    #def __str__(self):
    #    return str(self.datum)+" / "+str(self.cas)+" : "+self.tyma+"-"+self.tymb
    
    class Meta:
        verbose_name = "zápas"
        verbose_name_plural = "zápasy"


class Tipy(models.Model):
    jmeno = models.CharField(max_length=20, unique=True)
    tipy = models.CharField(max_length=70)

    class Meta:
        verbose_name = "tip"
        verbose_name_plural = "tipy"
        
    def __str__(self):
        return self.tipy