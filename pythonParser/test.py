import psycopg2
import psycopg2.extras

try:
    conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
    print("connect OK")
except:
    print("Не удалось подключиться к БД")
# Создаем курсор для работы
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

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

copyMusic()