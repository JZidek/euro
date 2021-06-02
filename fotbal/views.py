from django.shortcuts import render
import psycopg2
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as login_user
from django.contrib.auth.models import User
from .models import Zapasy_fotbal, Tipy_fotbal, Tymy_fotbal, Komenty
import datetime
import time
from django.db import connection
import operator


def sort_key(x):
    return x[3]

def login(request):
    userData = []
    data = []
    vysledky = []
    log = False
    test = []
    msg = ''
    admin = False
    
    for i in Zapasy_fotbal.objects.raw('SELECT id,datum,cas,skupina,tyma,tymb, scorea, scoreb, vysledek FROM fotbal_Zapasy_fotbal ORDER BY datum, cas DESC'):
        data.append([i.datum,i.cas,i.skupina,i.tyma,i.tymb,i.scorea,i.scoreb,i.vysledek])
        vysledky.append([i.scorea, i.scoreb])
        test.append(i.datum)
    
    if not request.user.is_authenticated:
        msg = "prihlaste se prosim..."
        log = False
    else:
        log = True
    if request.method == "POST":
        user = request.POST.get('user')
        passw = request.POST.get('pass')
        userData = [user, passw]
        

        if request.user.is_superuser:
            admin = True
        else:
            admin = False
        # prihlaseni uzivatele
        if request.POST.get('prihlaseni'):
            user_auth = authenticate(request, username=user, password= passw)
            # neregistrovany uzivatel
            
            if not user_auth:
                for i in data:
                    i[0] = i[0].strftime("%d.%m.")
                msg = "neznamy uzivatel nebo heslo, chcete zalozit noveho uzivatele?"
                return render(request, 'fotbal/zapasy_sk.html', dict(msg=msg, userData= userData, data=data, log=log, admin=admin))
            # registrovany uzivatel
            elif user_auth:
                login_user(request, user_auth)
                log = True
                msg = "Vítejte..."
                for i in Tipy_fotbal.objects.raw('SELECT id, Tipy_skore_sk FROM fotbal_Tipy_fotbal WHERE jmeno = %s',[str(request.user)]):
                    tip = i.tipy_skore_sk
                list1=[]
                list1 = tip.split(",")
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
                return render(request, 'fotbal/zapasy_sk.html', dict(msg=msg, userData= [request.user,"" ], data=data, log=log, admin=admin))
                     
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

                tip = Tipy_fotbal.objects.create(jmeno = user, tipy_skore_sk = "--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--,--")
                tip.save()
                msg = "Vase registrace byla uspesna, prihlaste se prosim"
            except:
                msg = "Uzivatelske jmeno jiz existuje, zvolte prosim jine"

        # zapis tipu uzivatele
        elif request.POST.get('tipy_zapis'):
            tipy = ''
            for i in range(36):
                a = request.POST.get('tipa.{0}'.format(i))
                b = request.POST.get('tipb.{0}'.format(i))
                try: 
                    int(a)
                    a = a[-1:]
                    tipy += a
                    int(b)
                    b = b[-1:]
                    tipy += b
                    tipy += ","
                except:
                    tipy += "--,"
            tipy = tipy[:-1]
            with connection.cursor() as cursor:
                cursor.execute('UPDATE fotbal_tipy_fotbal SET Tipy_skore_sk = %s WHERE jmeno = %s',[tipy, user])
            msg = 'tipy ulozeny'
            log = True
            
            for i in Tipy_fotbal.objects.raw('SELECT id, Tipy_skore_sk FROM fotbal_Tipy_fotbal WHERE jmeno = %s',[str(request.user)]):
                tip = i.tipy_skore_sk
            list1=[]
            list1 = tip.split(",")
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

            return render(request, 'fotbal/zapasy_sk.html', dict(msg=msg, userData= [request.user,"" ], data=data, log=log, admin=admin))
    
        elif request.POST.get('vyrazovak'):
            tymy = []
            for i in Tipy_fotbal.objects.raw('SELECT id, Tipy_skore_sk FROM fotbal_Tipy_fotbal WHERE jmeno = %s',[str(request.user)]):
                tip = i.tipy_skore_sk
            list1=[]
            list1 = tip.split(",")
            skA, skB, skC, skD, skE, skF = [],[],[],[],[],[]
            hra =[]
 
            try:
                temp = [int(i) for i in list1]
            
                for i in Tymy_fotbal.objects.raw('SELECT id, tym, skupina FROM fotbal_Tymy_fotbal'):
                    tymy.append([i.tym,0,0,0, i.skupina])
                for i, value in enumerate(data):
                    
                    for j in tymy:                        
                        if j[0] == value[3]:
                            j[1] += int(list1[i][:1])
                            j[2] += int(list1[i][1:])
                            if int(list1[i][:1]) > int(list1[i][1:]):
                                j[3] += 3
                            elif int(list1[i][:1]) < int(list1[i][1:]):
                                pass
                            else:
                                j[3] += 1
                        if j[0] == value[4]:
                            j[1] += int(list1[i][1:])
                            j[2] += int(list1[i][:1])
                            if int(list1[i][:1]) < int(list1[i][1:]):
                                j[3] += 3
                            elif int(list1[i][:1]) > int(list1[i][1:]):
                                pass
                            else:
                                j[3] += 1
                for i, value in enumerate(tymy):
                    if i in range(0,4):
                        skA.append(value)
                    elif i in range(4,8):
                        skB.append(value)   
                    elif i in range(8,12):
                        skC.append(value) 
                    elif i in range(12,16):
                        skD.append(value) 
                    elif i in range(16,18):
                        skE.append(value) 
                    elif i in range(18,22):
                        skF.append(value)  
                skA.sort(key=operator.itemgetter(3,1), reverse=True)
                skB.sort(key=operator.itemgetter(3,1), reverse=True)
                skC.sort(key=operator.itemgetter(3,1), reverse=True)
                skD.sort(key=operator.itemgetter(3,1), reverse=True)
                skE.sort(key=operator.itemgetter(3,1), reverse=True)
                skF.sort(key=operator.itemgetter(3,1), reverse=True)
                hra = [[skA[1][0],skB[1][0]] , [skA[0][0],skC[1][0]] , [skC[0][0],skD[2][0]] , [skB[0][0],skA[2][0]] , [skD[1][0],skE[1][0]] , [skF[0][0],skB[2][0]] , [skD[0][0],skF[1][0]] , [skE[0][0],skC[2][0]]]
            except:
                print("nejsou vyplneny vsechny zapasy")
            return render(request, 'fotbal/zapasy_vyraz.html', dict(msg=msg, userData= [request.user,"" ],log=log, hra=hra, admin=admin))
        
        elif request.POST.get('poradi'):
            tipy = []
            list2 = []
            score = []
            for i in Tipy_fotbal.objects.raw('SELECT * FROM fotbal_tipy_fotbal'):
                tipy.append([i.jmeno, i.tipy_skore_sk])
            for i, value in enumerate(tipy):
                x = 0
                jm = value[0]
                list2 = value[1].split(",")
                for j, value in enumerate(list2):
                    try:
                        if vysledky[j][0] == 100 or vysledky[j][1] == 100:
                            x = x
                        elif value[0] == str(vysledky[j][0]) and value[1] == str(vysledky[j][1]):
                            x +=3
                        elif (int(value[0]) < int(value[1]) and int(vysledky[j][0]) < int(vysledky[j][1])) or (int(value[0]) > int(value[1]) and int(vysledky[j][0]) > int(vysledky[j][1])) or (int(value[0]) == int(value[1]) and int(vysledky[j][0]) == int(vysledky[j][1])):
                            x +=1
                    except:
                        pass
                score.append([x, jm])
                score.sort(reverse=True)

            for i, value in enumerate(score):
                value.append(i+1)
            return render(request, 'fotbal/poradi.html', dict(msg=msg, userData= userData, score=score,log=log, admin=admin))

        elif request.POST.get('tabulky'):
            tymyA = []
            tymyB = []
            tymyC = []
            tymyD = []
            tymyE = []
            tymyF = []
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['A']):
                tymyA.append([int(i.skore), i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['B']):
                tymyB.append([i.skore, i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['C']):
                tymyC.append([i.skore, i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['D']):
                tymyD.append([i.skore, i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['E']):
                tymyE.append([i.skore, i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            for i in Tymy_fotbal.objects.raw('SELECT * FROM fotbal_Tymy_fotbal WHERE skupina = %s',['F']):
                tymyF.append([i.skore, i.skupina, i.tym, i.Z, i.V, i.R, i.P, i.Gdal, i.Gdostal])
            tymyA.sort(reverse=True)
            return render(request, 'fotbal/tabulky.html', dict(msg = msg, userData= [request.user,"" ], tymyA=tymyA,tymyB=tymyB,tymyC=tymyC,tymyD=tymyD,tymyE=tymyE,tymyF=tymyF, log=log, admin=admin))

        elif request.POST.get('update'):
            tymy = []
            for i in Tymy_fotbal.objects.raw('SELECT id, tym FROM fotbal_Tymy_fotbal'):
                tymy.append([i.tym,0,0,0,0,0,0,0])
            for i in data:
                if int(i[5]) != 100:
                    for j in tymy:                        
                        if j[0] == i[3]:
                            j[1] += 1
                            j[5] += i[5]
                            j[6] += i[6]
                            if i[5] > i[6]:
                                j[2] += 1
                                j[7] += 3
                            elif i[5] < i[6]:
                                j[4] += 1
                            else:
                                j[3] += 1
                                j[7] += 1
                        if j[0] == i[4]:
                            j[1] += 1
                            j[5] += i[6]
                            j[6] += i[5]
                            if i[5] < i[6]:
                                j[2] += 1
                                j[7] += 3
                            elif i[5] > i[6]:
                                j[4] += 1
                            else:
                                j[3] += 1
                                j[7] += 1

            with connection.cursor() as cursor:
                for i in tymy:
                    cursor.execute('UPDATE fotbal_Tymy_fotbal SET Z=%s, V=%s, R=%s, P=%s, Gdal=%s, Gdostal=%s, skore=%s  WHERE tym = %s',[i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[0]])
        
        elif request.POST.get('kom'):
            text = request.POST.get('koment')
            x = Komenty(jmeno=str(request.user) ,koment=text)
            x.save()
        
    # zmena formatu data
    if request.user.is_authenticated:
        for i in Tipy_fotbal.objects.raw('SELECT id, Tipy_skore_sk FROM fotbal_Tipy_fotbal WHERE jmeno = %s',[str(request.user)]):
            tip = i.tipy_skore_sk
        list1=[]
        list1 = tip.split(",")
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
            value.append(visibility)
            value.append(i)
    for i in data:
        i[0] = i[0].strftime("%d.%m.")
    return render(request, 'fotbal/zapasy_sk.html', dict(msg = msg, userData= [request.user,"" ], data=data, log=log, admin=admin))



