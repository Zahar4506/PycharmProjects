import string

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

# Список пользователей
audios1 = (
    # Id пользователй
    "475092562",
    "475148630",
    "475159239",
    "475172908",
    "475299098"
)
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

def program(audios):
    # Функции ---------------------------------------------------------------------------------------------------------

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
            #cur.execute("INSERT INTO public.vkuser (uservkid, fname, lname, city, faculty) VALUES ('" + str(userid) + "', '" + str(fname) + "', '" + str(lname) + "', '" + str(city) + "', '" + str(faculty) + "')")
            cur.execute("INSERT INTO public.city (id, name) VALUES ('" + str(cityid) + "', '" + str(title) + "')")
            #cur.execute("UPDATE public.city SET id='" + str(cityid) + "', name='" + str(title) + "' WHERE id = '"+str(cityid)+"'")
            conn.commit()
            print("Положил данные города (название) -> ", cityid," ", title)
            profiles = ""
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
                profiles = vk_api.users.get(user_id=userid, fields='city,connections,education,interests,sex,universities')
            except VkAPIError as e:
                print("================VK================",e)
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


            cur.execute("INSERT INTO public.vkuser (uservkid, fname, lname, city, faculty) VALUES ('" + str(userid) + "', '" + str(fname) + "', '" + str(lname) + "', '" + str(city) + "', '" + str(faculty) + "')")
            # Обновление БД из вк
            #cur.execute("UPDATE public.vkuser SET fname = '" + str(fname) + "', lname = '" + str(lname) + "', city = '" + str(city) + "', faculty = '" + str(faculty) + "' WHERE ""uservkid"" = " + str(userid) + "")
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
                    cur.execute("UPDATE public.vkuser SET fname = '" + str(fname) + "', lname = '" + str(lname) + "', city = '" + str(city) + "', faculty = '" + str(faculty) + "' WHERE ""uservkid"" = " + str(userid) + "")
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








    # --------------------------------------------------СТАРТ ПРОГРАММЫ ----------------------------------------------------
    start_time = time.time()
    try:
        conn = psycopg2.connect("dbname='reestr' user='postgres' host='127.0.0.1' password='1'")
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


    arrClean.clear()
    print(arrClean)
    print("--- %s seconds ---" % (time.time() - start_time))
    print("ПАУЗА 10")
    time.sleep(10)


    baseurl = "https://vk.com/"
    # username = "89821469162"
    username = "89505375037"
    # password = "Zx1#qwerty1906ugjoij"
    password = "Zx1$qwerty1906"

    xpaths = {
        'usernameTxtBox': "//*[@id='index_email']",
        'passwordTxtBox': "//*[@id='index_pass']",
        'submitButton': "//*[@id='index_login_button']"
    }

    #mydriver = webdriver.Firefox(executable_path=r'D:\parser\geckodriver.exe')
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
    # Закрываем соединение с БД
    cur.close()
    conn.close()


def main():
    with ThreadPoolExecutor(max_workers=3) as executor:
        executor.submit(program, (audios1))
    # executor.submit(program,(audios2))
    # executor.submit(program,(audios3))


# program(audios1)
if __name__ == '__main__':
    main()
