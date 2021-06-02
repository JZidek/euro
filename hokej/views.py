from django.shortcuts import render
import psycopg2
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
from .models import Zapasy, Tipy
import datetime
import time
from django.db import connection


def login(request):
    userData = []
    data = []
    vysledky = []
    log = False
    test = []
    msg = ''
    for i in Zapasy.objects.raw('SELECT id,datum,cas,skupina,tyma,tymb, scorea, scoreb, vysledek skupina FROM hokej_zapasy'):
        data.append([i.datum,i.cas,i.skupina,i.tyma,i.tymb,i.scorea,i.scoreb,i.vysledek])
        vysledky.append(i.vysledek)
        test.append(i.datum)
    print(request.user)
    if not request.user.is_authenticated:
        msg = "prihlas se prosim..."
        log = False
    else:
        log = True
    if request.method == "POST":
        user = request.POST.get('user')
        passw = request.POST.get('pass')
        userData = [user, passw]

        # prihlaseni uzivatele
        if request.POST.get('prihlaseni'):
            user_auth = authenticate(request, username=user, password= passw)
            if not user_auth:

                msg = "neznamy uzivatel nebo heslo, chcete zalozit noveho uzivatele?"
                return render(request, 'hokej/login.html', dict(msg=msg, userData= [request.user,"" ], data=data, log=log))
            elif user_auth:
                login_user(request, user_auth)
                log = True
                tip = Tipy.objects.raw('SELECT id, tipy FROM hokej_tipy WHERE jmeno = %s',[str(request.user)])
                tip = str(tip[0])
                list1=[]
                list1[:0]=tip
                msg = "Vítej zpět {0}".format(user)
                
                for i, value in enumerate(data):
                    visibility = False
                    value.append(list1[i])
                    
                    if value[0] < datetime.date.today():
                        visibility = False
                    elif (value[0] == datetime.date.today() and value[1] < datetime.datetime.now().time()):
                        visibility = False
                    else:
                        visibility = True
                    # zmena formatu data
                    if value[0] == datetime.date.today():
                        value[0] = "dnes"
                    else:
                        value[0] = value[0].strftime("%d.%m.")
                        value.append(visibility)
                        value.append(i)
                
                return render(request, 'hokej/zapasy_skupina.html', dict(msg=msg, userData= [request.user,"" ], data=data, log=log))
        
        # odhlaseni uzivatele
        elif request.POST.get('odhlaseni'):
            logout(request)
            msg = "Byl jste uspesne odhlasen"
            log = False
        
        # registrace uzivatele
        elif request.POST.get('registrace'):
            try:
                new_user = User.objects.create_user(user, '', passw)
                new_user.save()

                tip = Tipy.objects.create(jmeno = user, tipy = "----------------------------------------------------------------------")
                tip.save()
                msg = "Vase registrace byla uspesna, prihlaste se prosim"
            except:
                msg = "Uzivatelske jmeno jiz existuje, zvolte prosim jine"

        # zapis tipu uzivatele
        elif request.POST.get('tipy_zapis'):
            tipy = ''
            for i in range(56):
                s = request.POST.get('tip.{0}'.format(i))
                try: 
                    int(s)
                    s = s[-1:]
                    tipy += s
                except:
                    tipy += "-"
            with connection.cursor() as cursor:
                cursor.execute('UPDATE hokej_tipy SET tipy = %s WHERE jmeno = %s',[tipy, user])
            msg = 'tipy ulozeny'
            log = True
            tip = Tipy.objects.raw('SELECT id, tipy FROM hokej_tipy WHERE jmeno = %s',[user])
            tip = str(tip[0])
            list1=[]
            list1[:0]=tip
            for i, value in enumerate(data):
                visibility = False
                value.append(list1[i])
                
                if value[0] < datetime.date.today():
                    visibility = False
                elif (value[0] == datetime.date.today() and value[1] < datetime.datetime.now().time()):
                    visibility = False
                else:
                    visibility = True
                # zmena formatu data
                value[0] = value[0].strftime("%d.%m.")
                value.append(visibility)
                value.append(i)

            return render(request, 'hokej/zapasy_skupina.html', dict(msg=msg, userData= [], data=data, log=log))
    
        elif request.POST.get('vyrazovak'):
            return render(request, 'hokej/zapasy_vyraz.html', dict(msg=msg, userData= userData))
        
        elif request.POST.get('tabulky'):
            tipy = []
            list2 = []
            score = []
            for i in Tipy.objects.raw('SELECT * FROM hokej_tipy'):
                tipy.append([i.jmeno, i.tipy])
            for i, value in enumerate(tipy):
                jm = value[0]
                list2[0:2] = value[1]
                x = 0
                for j, value in enumerate(list2):
                    try:
                        if value == str(vysledky[j]):
                            x += 1
                    except:
                        break
                
                score.append([i+1,jm, x])

            return render(request, 'hokej/tabulky.html', dict(msg=msg, userData= userData, score=score))
    # zmena formatu data
    
    if request.user.is_authenticated:
        tip = Tipy.objects.raw('SELECT id, tipy FROM hokej_tipy WHERE jmeno = %s',[str(request.user)])
        tip = str(tip[0])
        list1=[]
        list1[:0]=tip
        msg = "Vítej zpět {0}".format(str(request.user))
        
        for i, value in enumerate(data):
            visibility = False
            value.append(list1[i])
            
            if value[0] < datetime.date.today():
                visibility = False
            elif (value[0] == datetime.date.today() and value[1] < datetime.datetime.now().time()):
                visibility = False
            else:
                visibility = True
            # zmena formatu data
            if value[0] == datetime.date.today():
                value[0] = "dnes"
            else:
                value[0] = value[0].strftime("%d.%m.")
                value.append(visibility)
                value.append(i)

    return render(request, 'hokej/zapasy_skupina.html', dict(msg = msg, userData= [request.user,"" ], data=data, log=log))


'''
def tabulky(request):

    user = request.POST.get('user')
    passw = request.POST.get('pass')
    userData = [user, passw]
  
    msg = "prihlas se prosim..."
    if request.method == "POST":
        user = request.POST.get('user')
        passw = request.POST.get('pass')
        userData = [user, passw]

        # prihlaseni uzivatele
        if request.POST.get('prihlaseni'):
            user_auth = authenticate(request, username=user, password= passw)
            if not user_auth:
                msg = "neznamy uzivatel nebo heslo, chcete zalozit noveho uzivatele?"
                return render(request, 'hokej/login.html', dict(msg=msg, userData= userData))
            elif user_auth:                
                msg = "Vítej zpět {0}".format(user)
                                
                return render(request, 'hokej/login.html', dict(msg=msg, userData= userData))
        
        # odhlaseni uzivatele
        elif request.POST.get('odhlaseni'):
            logout(request)
            msg = "Byl jste uspesne odhlasen"
        
        # registrace uzivatele
        elif request.POST.get('registrace'):
            try:
                new_user = User.objects.create_user(user, '', passw)
                new_user.save()

                tip = Tipy.objects.create(jmeno = user, tipy = "----------------------------------------------------------------------")
                tip.save()
                msg = "Vase registrace byla uspesna, prihlaste se prosim"
            except:
                msg = "Uzivatelske jmeno jiz existuje, zvolte prosim jine"

    return render(request, 'hokej/tabulky.html', dict(msg=msg, userData= userData))

'''
