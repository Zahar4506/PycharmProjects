import json
import string

import requests
from requests import request
from selenium import webdriver

import time

import psycopg2
import psycopg2.extras

import vk
import re
from vk.exceptions import VkAPIError
from concurrent.futures import ThreadPoolExecutor
import time
import os
import pylast

"""
установка для постргес библиотек CREATE EXTENSION fuzzystrmatch;
CREATE EXTENSION pg_trgm;

create index tsv_gin on musicband using gin(clear);

SELECT * FROM vkuser WHERE levenshtein(fname, 'ЮЛИЯ') <= 3

session = vk.Session(access_token='fe34dc9f0660284aa0caced7b2dbe57579a378b45f24a99ba490b124f02c90958f7b7f7df802fb7f80650')
vk_api = vk.API(session, v='5.71')
id=56833040
profiles = vk_api.users.get(user_id=id, fields='city,connections,education,interests,sex,universities')
print(profiles)
for i in profiles:
    print(i['id'])
    print(i['first_name'])
    print(i['last_name'])
    print(i['city'])
    print(i['city']['id'])
    print(i['city']['title'])
    print(i['university'])
    print(i['university_name'])
    print(i['faculty'])
    print(i['faculty_name'])
    print(i['universities'])
"""

"""
                                                    КОНЕКИ К БД
try:
    conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
except:
    print("Не удалось подключиться к БД")
# Создаем курсор для работы
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

"""

"""
try:
    cur.execute("SELECT * FROM musicband")
except:
    print("Запрос не удался")
# for row in cur:
#    print(row)
results = cur.fetchall()
for row in results:
    print(row['nameband'])
musicbandname = "VVVVVVVVV"
try:
    # Попожить найденную группу
    # cur.execute("INSERT INTO public.musicband(nameband) VALUES (upper('"+musicbandname+"'))")
    cur.execute(
        "INSERT INTO public.vkuser_musicband(vkuserid, musicbandid)	VALUES ('12', (SELECT musicbandid FROM public.musicband WHERE nameband = upper('" + musicbandname + "')))")
    conn.commit()
    print("Положил")
except psycopg2.DatabaseError as e:
    if conn:
        conn.rollback()
    print('Error %s' % e)
    print("Запрос INSERT не удался")
# INSERT INTO public.musicband(nameband) VALUES (upper('"+musicbandname+"'))
# "INSERT INTO public.vkuser_musicband(vkuserid, musicbandid)	VALUES ('12', (SELECT musicbandid FROM public.musicband WHERE nameband = upper('"+musicbandname+"')))"
"""

"""
print("тип arr:", type(results))
print("Кол-во полей с строке: ", len(results))
print("Доступ по индексу:", results[0][1])
#Вывод названий столбцов в бд

colnames = [desc[0] for desc in cur.description]
print(colnames)
print(results)
#Вывод результата из бд, криво будет работать если бд изменится
#TODO как обращаться к столбцу по имени?
for i in range(0, len(results)):
    print(results[i][1])

"""
# Список пользователей
# TODO сделать ввод из файла
# audios1 = (
#     # Id пользователй
#     "475092562",
#     "475148630",
#     "475159239",
#     "475172908",
#     "475299098"
# )
audios2 = (
    # Id пользователй
    "418103",
    "958361",
    "1682933",
    "2009733",
    "2162926",
    "2382569",
    "2391584",
    "2581020",
    "2596564",
    "2690294",
    "2775635",
    "2923622",
    "3119493",
    "3150068",
    "3280134",
    "3323590",
    "3447572"
)

audios3 = (
    # Id пользователй
    "5412124",
    "5422267",
    "5442916",
    "5475971",
    "5536760",
    "5668313",
    "5932067",
    "5952865",
    "6015895",
    "6072056",
    "6111076",
    "6210635"
)
arrClean = []


# Функция для запуска парсинга данных пользвателя
def program(audios):
    # -----------------------------------------ФУНКЦИИ------------------------------------------------------------------
    # Установить факультет
    def setFaculty(university, facultyid, faculty_name):
        print("старт факультета")
        try:
            session = vk.Session(
                access_token='fe34dc9f0660284aa0caced7b2dbe57579a378b45f24a99ba490b124f02c90958f7b7f7df802fb7f80650')
            vk_api = vk.API(session, v='5.71')
            print(university != 6666666, "универ равен 6666666?")
            print(university, "универ")
            faculty_name_copy = faculty_name
            if facultyid != 6666666:
                if university != 6666666:
                    print("зашло в проверку")
                    try:
                        facultyRes = vk_api.database.getFaculties(university_id=university)
                    except VkAPIError as e:
                        print("================VK================", e)
                    print(facultyRes, " результат запроса к апи УНИВЕР")
                    for i in facultyRes['items']:
                        try:
                            print(str(i['id']) == str(facultyid), " проверка ид факультета")
                            print(str(i['id']), " ===== ", facultyid, " ----- ", i['title'])
                            if str(i['id']) == str(facultyid):
                                faculty_name = i['title']
                                print(faculty_name)
                                break
                            else:
                                continue
                        except:
                            faculty_name = "6666666"
                            print("------")
                    else:
                        if faculty_name == 6666666:
                            faculty_name = faculty_name_copy
                else:
                    print("Не существующий университет")
                    faculty_name = "6666666"
            else:
                print("Не существующий факультет")
                faculty_name = "6666666"

            # Попожить факультет
            # Код для вставки
            # Обновление БД из вк
            print("ФАКУЛЬТЕТ = ", facultyid, " НАЗВАНИЕ = ", faculty_name)
            cur.execute("INSERT INTO public.faculty (facultyid, name) VALUES ('" + str(facultyid) + "', '" + str(
                faculty_name) + "')")
            # cur.execute("UPDATE public.faculty SET facultyid = '" + str(facultyid) + "', name = '" + str(faculty_name) + "' WHERE ""facultyid"" = " + str(facultyid) + "")
            conn.commit()
            print("Положил данные факультета (название)-> ", facultyid, " ", faculty_name)
            facultyRes = None
        except (psycopg2.DatabaseError, VkAPIError) as e:
            if conn:
                conn.rollback()
            print(e.pgcode, " КОД ОШИБКИ")
            print('Error %s' % e)
            print("Запрос INSERT факультета не удался")
            if e.pgcode == "23505":
                try:
                    print("ПРОБУЕМ ОБНОВИТЬ Факультет")
                    cur.execute("UPDATE public.faculty SET facultyid = '" + str(facultyid) + "', name = '" + str(
                        faculty_name) + "' WHERE ""facultyid"" = " + str(facultyid) + "")
                    conn.commit()
                except psycopg2.DatabaseError as e:
                    if conn:
                        conn.rollback()
                    print("Запрос UPDATE факультета не удался")
        print("факультет финиш")

    def setCity(cityid):
        print("старт сити")
        try:
            session = vk.Session(
                access_token='fe34dc9f0660284aa0caced7b2dbe57579a378b45f24a99ba490b124f02c90958f7b7f7df802fb7f80650')
            vk_api = vk.API(session, v='5.71')
            try:
                cityRes = vk_api.database.getCitiesById(city_ids=cityid)
            except VkAPIError as e:
                print("================VK================", e)
            print(cityRes, "запрос к апи СИТИ")
            for i in cityRes:
                try:
                    title = i['title']
                    print("ДЛИНА СТРОКИ", len(title), len(title) == 0)
                    if len(title) == 0:
                        title = "6666666"
                    print(title, " <- Название города")
                except:
                    title = "6666666"
            # Попожить город
            # Код для вставки
            print("ГОРОД = ", cityid, "НАЗВАНИЕ =", title)
            # cur.execute("INSERT INTO public.vkuser (uservkid, fname, lname, city, faculty) VALUES ('" + str(userid) + "', '" + str(fname) + "', '" + str(lname) + "', '" + str(city) + "', '" + str(faculty) + "')")
            cur.execute("INSERT INTO public.city (id, name) VALUES ('" + str(cityid) + "', '" + str(title) + "')")
            # cur.execute("UPDATE public.city SET id='" + str(cityid) + "', name='" + str(title) + "' WHERE id = '"+str(cityid)+"'")
            conn.commit()
            print("Положил данные города (название) -> ", cityid, " ", title)
            profiles = None
            time.sleep(0.33)
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print('Error %s' % e)
            print("Запрос INSERT города не удался")
        print("Фиинишь город")

    def setUserInfo(userid):
        print("старт занесения информации о пользователе")
        try:
            session = vk.Session(
                access_token='fe34dc9f0660284aa0caced7b2dbe57579a378b45f24a99ba490b124f02c90958f7b7f7df802fb7f80650')
            vk_api = vk.API(session, v='5.71')
            try:
                profiles = vk_api.users.get(user_id=userid,
                                            fields='city,connections,education,interests,sex,universities')
            except VkAPIError as e:
                print("================VK================", e)
            print(profiles)
            for i in profiles:
                try:
                    fname = i['first_name']
                    print(fname)
                except:
                    fname = "null"
                try:
                    lname = i['last_name']
                    print(lname)
                except:
                    lname = "null"
                try:
                    city = i['city']['id']
                    print(city)
                except:
                    city = "6666666"
                try:
                    university = i['university']
                    if university == 0:
                        universityArr = i['universities']
                        if universityArr != []:
                            for j in universityArr:
                                university = j['id']
                        else:
                            university = "6666666"
                    print(university, " - универ")
                except:
                    university = "6666666"
                try:
                    faculty = i['faculty']
                    if faculty == 0:
                        facultyArr = i['universities']
                        if facultyArr != []:
                            for j in facultyArr:
                                faculty = j['faculty']
                        else:
                            faculty = "6666666"
                    print(faculty)
                except:
                    faculty = "6666666"
                try:
                    faculty_name = i['faculty_name']
                    print(faculty_name)
                except:
                    faculty_name = "6666666"
            # Попожить пользователя
            # Код для вставки TODO вставить в основной код программы при выполнении запроса к обновлению
            setCity(str(city))
            print(university, "универ для функции вставки и факультет", faculty, faculty_name)
            setFaculty(str(university), str(faculty), str(faculty_name))
            cur.execute("INSERT INTO public.vkuser (uservkid, fname, lname, city, faculty) VALUES ('" + str(
                userid) + "', '" + str(fname) + "', '" + str(lname) + "', '" + str(city) + "', '" + str(faculty) + "')")
            # Обновление БД из вк
            # cur.execute("UPDATE public.vkuser SET fname = '" + str(fname) + "', lname = '" + str(lname) + "', city = '" + str(city) + "', faculty = '" + str(faculty) + "' WHERE ""uservkid"" = " + str(userid) + "")
            conn.commit()
            print("Положил данные пользователя(имя, город, факультет) setInfoUser")
            profiles = ""
        except (psycopg2.DatabaseError, psycopg2.Error) as e:
            if conn:
                conn.rollback()
            print(e.pgcode, " КОД ОШИБКИ")
            print('Error %s' % e)
            if e.pgcode == "23505":
                try:
                    print("ПРОБУЕМ ОБНОВИТЬ")
                    cur.execute("UPDATE public.vkuser SET fname = '" + str(fname) + "', lname = '" + str(
                        lname) + "', city = '" + str(city) + "', faculty = '" + str(
                        faculty) + "' WHERE ""uservkid"" = " + str(userid) + "")
                    conn.commit()
                except psycopg2.DatabaseError as e:
                    if conn:
                        conn.rollback()
                    print("Запрос UPDATE пользователя не удался setInfoUser")
        print("финишь вставки пользователя")
        time.sleep(0.3)

    # Функиця установки музыки в бд
    # Заносим в БД в верхнем регистре
    def setMusic(musicbandname):
        try:
            # Попожить найденную группу
            cur.execute("INSERT INTO public.musicband(nameband) VALUES (upper('" + musicbandname + "'))")
            conn.commit()
            print("Положил в БД группу")
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print('Error %s' % e)
            print("Запрос INSERT музыкальной группы не удался")

    # Функция занесения связки пользователь-музыкальная группа в БД
    def setUserMusic(userid, musicbandname):
        try:
            # Попожить связку userid musicbamdname группу
            cur.execute(
                "INSERT INTO public.vkuser_musicband(vkuserid, musicbandid)	VALUES ('" + userid + "', (SELECT musicbandid FROM public.musicband WHERE nameband = upper('" + musicbandname + "')))")
            conn.commit()
            print("Положил")
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print('Error %s' % e)
            print("Запрос INSERT пользователя-музыка не удался")

    # Функция занесения пользователя в БД
    def setUser(userid):
        try:
            # Попожить пользователя
            # TODO имя пользователя?
            cur.execute("INSERT INTO public.vkuser (uservkid) VALUES ('" + userid + "')")
            conn.commit()
            print("Положил пользователя")
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print('Error %s' % e)
            print("Запрос INSERT пользователя не удался")

    # Функиця парсинг найденного массива музыкальных групп
    def viewMusic(array):
        for i in range(0, len(array)):
            setMusic(array[i].text)
            print(i, array[i].text)
            setUserMusic(audio, array[i].text)

    # Функция очистки музыкальных исполнителей
    def cleaningMusicBand(nameband):
        try:
            result = re.sub(r'[^a-zA-Zа-яА-Я0-9( )ёЁ]', ' ', nameband)
            result = re.sub(r'OST', '', result)
            result = re.sub(r'[()_]', ' ', result)
            result = re.sub(r'\s+', ' ', result)
            resFind = result.find('FEAT')
            if resFind != -1:
                result = result[0:resFind:1]
                print(resFind, "-----------FEAT")
            resFind = result.find('GLOBAL TUNING')
            if resFind != -1:
                result = result[resFind + 13:len(result):1]
                print(resFind, "-----------GLOBAL TUNING")
            resFind = result.find('FT')
            if resFind != -1:
                if result.find("DAFT") != -1:
                    print("daft")
                elif result.find("DRIFTMOON") != -1:
                    print("driftmoon")
                elif result.find("FIFTH HARMONY") != -1:
                    print("FIFTH HARMONy")
                else:
                    result = result[0:resFind:1]
                    print(resFind, "-----------FT")
            resFind = result.find('HZ ')
            if resFind != -1:
                result = result[resFind + 3:len(result):1]
                print(resFind, "<========hz")
                resFind = result.find('HZ ')
                if resFind != -1:
                    result = result[resFind + 3:len(result):1]
                    print(resFind, "<========hz2")
            resFind = result.find('CARMUSICKZ')
            if resFind != -1:
                result = result[resFind + 10:len(result):1]
                print(resFind, "<========carmuzic")
            resFind = result.find('CLUB RAЙ')
            if resFind != -1:
                result = result[resFind + 8:len(result):1]
                print(resFind, "<========CLUB RAЙ")
            resFind = result.find('145MUSIC')
            if resFind != -1:
                result = result[resFind + 8:len(result):1]
                print(resFind, "<========145MUSIC")
            result = re.sub(r'VKCOMSADINSTR', ' ', result)
            result = re.sub(r'VKHPNET', ' ', result)
            result = re.sub(r'МУЗЫКА', ' ', result)
            result = re.sub(r'НОВИНКА', ' ', result)
            result = re.sub(r'НОВИНКИ', ' ', result)
            result = re.sub(r'РИНГТОН', ' ', result)
            result = re.sub(r'ХИТ', ' ', result)
            result = re.sub(r'ХИТЫ', ' ', result)
            result = re.sub(r'EUROPA PLUS', ' ', result)
            result = re.sub(r'МЕСТО', ' ', result)
            result = re.sub(r'RADIO RECORD', ' ', result)
            result = re.sub(r'BOMBAFM', ' ', result)
            result = re.sub(r'CLUB', ' ', result)
            result = re.sub(r'DEEP HOUSE', ' ', result)
            result = re.sub(r'DFM', ' ', result)
            result = re.sub(r'EUROVISION', ' ', result)
            result = re.sub(r'FDM', ' ', result)
            result = re.sub(r'BPANMUSIC', ' ', result)
            result = re.sub(r'MUZMORU', ' ', result)
            result = re.sub(r'MS', ' ', result)
            result = re.sub(r'MUSIC', ' ', result)
            result = re.sub(r'[\d]', '', result)
            result = re.sub(r'\s+', ' ', result)
            if len(result) > 25:
                result = result[0:25:1]
            if len(result) < 2:
                result = ''
            else:
                return result
        except:
            print("очитска трека упала")
            return nameband

    # Функция очистки через Левенштейна
    def cleaningMusicClear(nameband):
        try:
            cur.execute("SELECT musicbandid, clearnameband, levenshtein('" + str(
                nameband) + "', clearnameband) as sml FROM musicband WHERE levenshtein('" + str(
                nameband) + "', clearnameband) = 1 ORDER BY  sml, clearnameband")
            results = cur.fetchall()
            print(results)
            if results == []:
                print('ПУСТО')
            else:
                for j in results:
                    print(j[0], j[1], j[2])
                    arrClean.append(j[0])
                    cur.execute(
                        "UPDATE musicband SET clear = '" + str(j[1]) + "' WHERE musicbandid ='" + str(j[0]) + "'")
                    conn.commit()
        except:
            print("очитска трека упала")

    # Функция разбиения факультетов на категории
    def categoryFaculty(faculty):
        try:
            print(faculty)
            for j in faculty:
                j[1] = j[1].upper()
                print(j[0], j[1])
                if j[1].find('ЖУРНА') > -1 or j[1].find('УПРАВЕНИЕ') > -1 or j[1].find('СОЦ') > -1 or j[1].find(
                        'ФИЛОЛ') > -1 or j[1].find('ЯЗЫК') > -1 or j[1].find('СПОРТ') > -1 or j[1].find('ТУРИЗ') > -1 or \
                        j[1].find('ДИЗАЙ') > -1 or j[1].find('МУНИЦ') > -1 or j[1].find('ГУМАН') > -1 or j[1].find(
                    'ВОКАЛ') > -1 or j[1].find('ПСИХО') > -1 or j[1].find('ПЕДАГ') > -1 or j[1].find(
                    'ФИЗИЧЕСКОЙ') > -1 or j[1].find('РУССК') > -1 or j[1].find('ЛИТЕРАТ') > -1:
                    print(j[1], "<========Гуманитарный")
                    cur.execute("UPDATE faculty SET category = '1' WHERE facultyid ='" + str(j[0]) + "'")
                elif j[1].find('МЕНЕДЖ') > -1 or j[1].find('ФИНАН') > -1 or j[1].find('ЭКОНОМ') > -1:
                    print(j[1], "<========Менеджмента и экономики")
                    cur.execute("UPDATE faculty SET category = '2' WHERE facultyid ='" + str(j[0]) + "'")
                elif j[1].find('ПРАВО') > -1 or j[1].find('ЮРИД') > -1 or j[1].find('ПРАВА') > -1 or j[1].find(
                        'АРБИТ') > -1 or j[1].find('АДВОКА') > -1 or j[1].find('УГОЛОВ') > -1 or j[1].find(
                    'ФИЛОС') > -1 or j[1].find('ИСТОР') > -1 or j[1].find('ЮРИС') > -1:
                    print(j[1], "<========Юридический")
                    cur.execute("UPDATE faculty SET category = '3' WHERE facultyid ='" + str(j[0]) + "'")
                elif j[1].find('БИОЛ') > -1 or j[1].find('ЕСТЕСТ') > -1 or j[1].find('ГЕОЛ') > -1 or j[1].find(
                        'НЕФТ') > -1 or j[1].find('ГАЗА') > -1 or j[1].find('БУРЕ') > -1 or j[1].find('АВТОМ') > -1 or \
                        j[1].find('ХИМИ') > -1 or j[1].find('ЭКОЛО') > -1 or j[1].find('ПРИРОДО') > -1 or j[1].find(
                    'ЭНЕРГЕ') > -1 or j[1].find('НЕФТЕ') > -1:
                    print(j[1], "<========Природопользование")
                    cur.execute("UPDATE faculty SET category = '4' WHERE facultyid ='" + str(j[0]) + "'")
                elif j[1].find('МАТЕМ') > -1 or j[1].find('ТЕХН') > -1 or j[1].find('ЭЛЕКТ') > -1 or j[1].find(
                        'СИСТЕМ') > -1 or j[1].find('ВЫЧИСЛИ') > -1 or j[1].find('ИНЖЕН') > -1 or j[1].find(
                    'ИНФОРМ') > -1 or j[1].find('МОДЕЛИ') > -1 or j[1].find('СТРОИТ') > -1 or j[1].find(
                    'ФИЗИК') > -1 or j[1].find('ТЕХНИЧ') > -1 or j[1].find('ТЕХНОЛОГ') > -1 or j[1].find('ТРАНСПОРТ') > -1:
                    print(j[1], "<========ИТСИТ")
                    cur.execute("UPDATE faculty SET category = '5' WHERE facultyid ='" + str(j[0]) + "'")
                else:
                    print('Неизвестное сочетание')
                    cur.execute("UPDATE faculty SET category = '0' WHERE facultyid ='" + str(j[0]) + "'")
            conn.commit()
        except:
            print("факультет упал")




    def getTegLast():
        try:
            cur.execute("SELECT idmusicbandnew,namemusicbandnew FROM newmusicband order by namemusicbandnew")
            results = cur.fetchall()
            print(results)
        except psycopg2.DatabaseError as e:
            if conn:
                conn.rollback()
            print('Error %s' % e)
            print("ЧТО то пошло не так")
        try:
            for index,artist in enumerate(results):
                print(index, '#')
                try:
                    s = requests.get('http://ws.audioscrobbler.com/2.0/?method=artist.getTopTags&artist=' + str(
                        artist[1]) + '&user=RJ&api_key=2136682266013c069f6907b81f140ec8&format=json')
                    json_date = json.loads(s.text)
                    print(json_date["toptags"]["tag"][0]["name"])
                    try:
                        cur.execute("UPDATE newmusicband SET tag = ('" + str(json_date["toptags"]["tag"][0]["name"]) + "') WHERE idmusicbandnew ='" + str(artist[0]) + "'")
                        conn.commit()
                    except psycopg2.DatabaseError as e:
                        print("error", e)
                        if conn:
                            conn.rollback()
                except Exception as e:
                    print("Пусто",e)
        except Exception as e:
            print("ошибка", e)
    # --------------------------------------------------СТАРТ ПРОГРАММЫ ------------------------------------------------

    start_time = time.time()
    print("cnfht")

    try:
        conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
        print("connect OK")
    except:
        print("Не удалось подключиться к БД")
    # Создаем курсор для работы
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    """
    try:
        cur.execute("SELECT uservkid FROM public.vkuser")
        # cur.execute("SELECT city FROM public.vkuser WHERE city IS NOT NULL GROUP BY city ORDER BY city DESC")
        results = cur.fetchall()
        print(results)
        for j in results:
            print(j[0])
            setUserInfo(j[0])
    except psycopg2.DatabaseError as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        print("ЧТО то пошло не так")
    """



    # запрос на апдейт музыки через левенштейна
    #     try:
    #         cur.execute("SELECT musicbandid, clearnameband FROM musicband WHERE clearnameband != '' ORDER BY clearnameband")
    #         results = cur.fetchall()
    #         print(results)
    #         for index, j in enumerate(results):
    #             print(index, '<<<<<<<<<<<<<<  ', j[0], j[1])
    #             print(arrClean)
    #             print(arrClean.count(j[0]) != 0, ' = = = = = =  = = = = =  = =')
    #             if arrClean.count(j[0]) != 0:
    #                 continue
    #             if j[1] != str('None'):
    #                 cleaningMusicClear(j[1])
    #                 print(">>>>>>>>>>>>>>>>>>>>>>ДАНННЫЕ ПОСЛЕ ОЧИСТКИ")
    #             else:
    #                 print('Встретился none')
    #     except psycopg2.DatabaseError as e:
    #         if conn:
    #             conn.rollback()
    #         print('Error %s' % e)
    #         print("ЧТО то пошло не так")

    # запрос на апдейт факультетеов
    # try:
    #     cur.execute("SELECT facultyid, name FROM faculty ORDER BY name")
    #     results = cur.fetchall()
    #     print(results)
    #     categoryFaculty(results)
    #
    # except psycopg2.DatabaseError as e:
    #     if conn:
    #         conn.rollback()
    #     print('Error %s' % e)
    #     print("ЧТО то пошло не так")

    # Функция копирования музыки чистой в чистую таблицу
    def copyMusic():
        try:
            cur.execute("SELECT musicbandid, clearnameband FROM musicband   ORDER BY clearnameband")
            results = cur.fetchall()
            print(results)
            for j in results:
                print(j[0], j[1])
                try:
                    cur.execute(
                        "INSERT INTO newmusicband(idmusicbandnew, namemusicbandnew)	VALUES (" + str(j[0]) + ",'"
                        + str(j[1]) + "')")
                    conn.commit()
                    print(" копи пользователя ")
                    copyUser(str(j[0]), str(j[1]), True)
                except psycopg2.DatabaseError as e:
                    if conn:
                        conn.rollback()
                    print("Ошибка = ", e)
                    print(" копи пользователя! ")
                    copyUser(str(j[0]), str(j[1]), False)
        except (psycopg2.DatabaseError) as e:
            if conn:
                conn.rollback()
            print(e.pgcode, " КОД ОШИБКИ")
            print('Error %s' % e)
            print("Запрос INSERT copyMusic упал")

    # Функция копии пользователя в новую таблицу
    def copyUser(musicid, musicname, a):
        if a == True:
            try:
                cur.execute(
                    "SELECT vkuserid, musicbandid FROM vkuser_musicband WHERE musicbandid = " + str(musicid) + "")
                conn.commit()
                resul = cur.fetchall()
                print(resul)
                for i in resul:
                    try:
                        cur.execute(
                            "INSERT INTO vkuser_clearmusicbandnew(idvkuser, idclear) VALUES (" + str(i[0]) + ",'"
                            + str(i[1]) + "')")
                        conn.commit()
                    except psycopg2.DatabaseError as e:
                        if conn:
                            conn.rollback()
                        print(e.pgcode, " <<<<<<<<<<????КОД ОШИБКИ")
                        print('Error %s' % e)
            except:
                if conn:
                    conn.rollback()
                print("ошибочка")
        else:
            print("Копия копии")
            try:
                cur.execute("SELECT idmusicbandnew FROM newmusicband WHERE namemusicbandnew = '" + str(musicname) + "'")
                conn.commit()
                idmnim = cur.fetchall()
                print(idmnim)
                print(idmnim[0][0])
                cur.execute(
                    "SELECT vkuserid, musicbandid FROM vkuser_musicband WHERE musicbandid = " + str(musicid) + "")
                conn.commit()
                resul = cur.fetchall()
                print(resul)
                for i in resul:
                    try:
                        cur.execute(
                            "INSERT INTO vkuser_clearmusicbandnew(idvkuser, idclear) VALUES (" + str(i[0]) + ",'"
                            + str(idmnim[0][0]) + "')")
                        conn.commit()
                    except psycopg2.DatabaseError as e:
                        if conn:
                            conn.rollback()
                        print(e.pgcode, " <<<<<<<<<<????КОД ОШИБКИ")
                        print('Error %s' % e)
            except:
                if conn:
                    conn.rollback()
                print("ошибочка")
        pass

    getTegLast()
    time.sleep(10)
    copyMusic()
    # try:
    #     cur.execute("SELECT clearnameband, musicbandid FROM musicband ORDER BY clearnameband")
    #     results = cur.fetchall()
    #     print(results)
    #     for j in results:
    #         print("вход в обработчик")
    #         try:
    #             print(j[0], j[1])
    #             cur.execute("INSERT INTO newmusicband(idmusicbandnew, namemusicbandnew)	VALUES (" + str(j[1]) + ",'" + str(j[0]) + "')")
    #             print("Запрос пошел")
    #             conn.commit()
    #             print("commit")
    #             try:
    #                 print("зашли в апдейт пользователя")
    #                 cur.execute("SELECT vkuserid, musicbandid FROM vkuser_musicband WHERE musicbandid = "+str(j[1])+"")
    #                 conn.commit()
    #                 resul = cur.fetchall()
    #                 print(resul)
    #                 for i in resul:
    #                     print("вход в обработчик")
    #                     try:
    #                         print("==================")
    #                         cur.execute(
    #                             "INSERT INTO vkuser_clearmusicbandnew(idvkuser, idclear) VALUES (" + str(i[0]) + ",'" + str(i[1]) + "')")
    #                         conn.commit()
    #                     except psycopg2.DatabaseError as e:
    #                         if conn:
    #                             conn.rollback()
    #                         print(e.pgcode, " <<<<<<<<<<????КОД ОШИБКИ")
    #                         print('Error %s' % e)
    #             except:
    #                 print("ошибочка")
    #         except psycopg2.DatabaseError as er:
    #             if conn:
    #                 conn.rollback()
    #             print(er.pgcode, " <<<<<<<<<<КОД ОШИБКИ")
    #             print('Error %s' % er)
    #             print("Запрос INSERT музыканта не удался")
    #             if er.pgcode == "23505":
    #                 print("ОШИБКАААААААААА++++++++++++++++++++++++++++++++++")
    #                 cur.execute("SELECT musicbandid, clearnameband FROM musicband WHERE clearnameband = '"+str(j[0])
    #                               +"' ORDER BY clearnameband LIMIT 1")
    #                 conn.commit()
    #                 result = cur.fetchall()
    #                 print(result, '////////////////////////')
    #                 print(result[0][0], '////////////////////////',result[0][1])
    #                 try:
    #                     print("зашли в апдейт пользователя")
    #                     cur.execute(
    #                         "SELECT vkuserid, musicbandid FROM vkuser_musicband WHERE musicbandid = " + str(result[0][0]) + "")
    #                     conn.commit()
    #                     resul = cur.fetchall()
    #                     print(resul)
    #                     for i in resul:
    #                         print("вход в обработчик")
    #                         try:
    #                             print("==================")
    #                             cur.execute(
    #                                 "INSERT INTO vkuser_clearmusicbandnew(idvkuser, idclear) VALUES (" + str(
    #                                     i[0]) + ",'" + str(i[1]) + "')")
    #                             conn.commit()
    #                             print("удачно")
    #                         except psycopg2.DatabaseError as e:
    #                             if conn:
    #                                 conn.rollback()
    #                             print(e.pgcode, " <<<<<<<<<<????КОД ОШИБКИ")
    #                             print('Error %s' % e)
    #                 except:
    #                     print("ошибочка")
    #
    # except (psycopg2.DatabaseError) as e:
    #     if conn:
    #         conn.rollback()
    #     print(e.pgcode, " КОД ОШИБКИ")
    #     print('Error %s' % e)
    #     print("Запрос INSERT факультета не удался")
    #     if e.pgcode == "23505":
    #         print("ОШИБКАААААААААА")

    arrClean.clear()
    print(arrClean)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print("ПАУЗА 10")
    # time.sleep(10)

    baseurl = "https://vk.com/"
    username = "89505375037"
    password = "Zx1$qwerty1906"

    xpaths = {
        'usernameTxtBox': "//*[@id='index_email']",
        'passwordTxtBox': "//*[@id='index_pass']",
        'submitButton': "//*[@id='index_login_button']"
    }

    # mydriver = webdriver.Firefox(executable_path=r'D:\parser\geckodriver.exe')
    # os.environ['MOZ_HEADLESS'] = '1'
    mydriver = webdriver.Firefox(executable_path=r'D:\parser\geckodriver.exe')
    # mydriver = webdriver.PhantomJS(executable_path=r'C:\Users\Zleha\PycharmProjects\pythonParser')
    mydriver.get(baseurl)
    # time.sleep(5)
    # mydriver.maximize_window()

    mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).clear()
    mydriver.find_element_by_xpath(xpaths['usernameTxtBox']).send_keys(username)
    mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).clear()
    mydriver.find_element_by_xpath(xpaths['passwordTxtBox']).send_keys(password)
    mydriver.find_element_by_xpath(xpaths['submitButton']).click()

    print('тормозим')
    time.sleep(5)
    print('поехали')

    # Разбираем список пользователей
    for audio in audios:
        urlaudio = baseurl + 'audios' + audio
        try:
            mydriver.get(urlaudio)
            print(urlaudio)
            print(mydriver.current_url)
            if urlaudio == mydriver.current_url:
                for i in range(100):
                    mydriver.execute_script("window.scrollBy(0,1000)")
                setUser(audio)
                setUserInfo(audio)
                content = mydriver.find_elements_by_css_selector('a.audio_row__performer')
                print("\nКоличество треков = ", len(content))
                viewMusic(content)
                print("sleep")
                time.sleep(0.5)
            else:
                print("Доступ к аудио закрыт id", audio)
                continue
        except:
            print("Не удалось обратиться к url")
            continue
        print("REFRESH страницы")
        mydriver.refresh()

    # ---------------------------------ОЧИИСТКА ПЕРВОНАЧАЛЬНАЯ ОТ МУСОРА РЕГУЛЯРКА--------------------------------------
    try:
        cur.execute("SELECT musicbandid, nameband FROM musicband")
        results = cur.fetchall()
        print(results)
        for j in results:
            print(j[0], j[1])
            clearnameband = cleaningMusicBand(j[1])
            print(clearnameband)
            try:
                cur.execute("UPDATE musicband SET clearnameband = ltrim('" + str(clearnameband) + "') WHERE musicbandid ='"+str(j[0])+"'")
                conn.commit()
            except:
                print("error")
            print("положил---------------------")
    except psycopg2.DatabaseError as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        print("ЧТО то пошло не так")

    # Закрываем соединение с БД
    cur.close()
    conn.close()
    print("FINISH")


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(program, ())
    # executor.submit(program,(audios2))
    # executor.submit(program,(audios3))


# # program(audios1)
if __name__ == '__main__':
    main()
