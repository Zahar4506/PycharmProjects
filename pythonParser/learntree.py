import csv
from contextlib import contextmanager

import pandas as pd
import numpy as np
import warnings

import matplotlib.pyplot as plt
import psycopg2
import psycopg2.extras
import pydotplus
import time
import pickle


warnings.filterwarnings("ignore")

from sklearn import tree

import graphviz
from sklearn.model_selection import train_test_split, StratifiedKFold, KFold
from sklearn.metrics import accuracy_score, f1_score, average_precision_score, recall_score, precision_score
from sklearn.model_selection import GridSearchCV, cross_val_score

# 1-Гуманитарный
# 2-Менеджмент и экономика
# 3-Юридический
# 4-Природопользования
# 5-ИТСИТ

dumpfile = None

# def tableLearn(categ):
#     try:
#         conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
#         print("connect OK")
#     except:
#         print("Не удалось подключиться к БД")
#     # Создаем курсор для работы
#     cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
#     try:
#         if categ == 0:
#             cur.execute("SELECT uservkid, f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE v.category = "+str(categ)+" and f.category != 0 order by uservkid")
#         else:
#             cur.execute("SELECT uservkid, f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE v.category = " + str(categ) + " and f.category != 1 order by uservkid")
#         users = cur.fetchall()
#         print(users)
#         cur.execute("SELECT idmusicbandnew FROM newmusicband order by idmusicbandnew")
#         musicband = cur.fetchall()
#         print(musicband)
#     except:
#         print('Сломалася')
#     svaz = [[5587], [5588]]
#     print("START")
#     # +1 для замены последнего значения на выбранную специальность
#     dfaALL = numpy.zeros((len(musicband)+1), dtype=numpy.uint8)
#     dfaUser = numpy.zeros((len(users)), dtype=numpy.uint32)
#     for indexU, j in enumerate(users):
#         dfa = numpy.zeros((len(musicband) + 1), dtype=numpy.uint8)
#         try:
#             cur.execute("SELECT idclear FROM vkuser_clearmusicbandnew WHERE idvkuser = "+str(j[0])+" order by idclear")
#             svaz = cur.fetchall()
#             print(svaz)
#         except:
#             print("запрос списка связи упал")
#         try:
#             cur.execute("SELECT f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE uservkid = "+str(j[0])+"")
#             category = cur.fetchall()
#
#         except:
#             print("запрос списка связи упал")
#         print(indexU, "< USER")
#         for indexM, i in enumerate(musicband):
#             for indexS, k in enumerate(svaz):
#                 try:
#                     if i.index(k[0])==0:
#                         print("----------------------------------")
#                         dfa[indexM] = 1
#                     break
#                 except ValueError as e:
#                     print("ERROR > ",e)
#         dfa[len(musicband)] = category[0][0]
#         print(j[0])
#         dfaUser[indexU] = j[0]
#         print(dfaUser)
#         print("ТАБЛИЦА\n", dfaALL)
#         dfaau = pd.DataFrame(dfaUser)
#         print(dfaau)
#         dfaALL = numpy.vstack((dfaALL, dfa))
#         dfaa = pd.DataFrame(dfaALL)
#         print(dfaa)
#         time.sleep(1)
#         try:
#             print("ЗАПИСЬ")
#             if categ == 0:
#                 dfaau.to_csv('files/outputUser.csv')
#                 dfaa.to_csv('files/output.csv')
#                 print("ЗАПИСАНО")
#             else:
#                 dfaau.to_csv('files/output1User.csv')
#                 dfaa.to_csv('files/output1.csv')
#                 print("ЗАПИСАНО 1")
#         except:
#             print("Упала запись в файл")
#         time.sleep(1)


def tableLearn(categ):
    try:
        conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
        print("connect OK")
    except:
        print("Не удалось подключиться к БД")
    # Создаем курсор для работы
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    try:
        if categ == 0:
            cur.execute("SELECT uservkid, f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE v.category = "+str(categ)+" and f.category != 0 order by uservkid")
        else:
            cur.execute("SELECT uservkid, f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE v.category = " + str(categ) + " and f.category != 1 order by uservkid")
        users = cur.fetchall()
        print(users)
        if categ == 0:
            # cur.execute("SELECT idmusicbandnew FROM newmusicband order by idmusicbandnew")
            cur.execute("SELECT idclear FROM vkuser_clearmusicbandnew GROUP BY idclear HAVING count(*)> 10 and count(*)<1000 ORDER BY count(*) DESC")
     #        cur.execute("""SELECT musicbandid FROM public.musicband WHERE nameband LIKE ANY(array['ЛЕНИНГРАД','КИНО','СПЛИН','IMAGINE DRAGONS','ЗЕМФИРА','ДДТ','ПИКНИК','QUEEN','АГАТА КРИСТИ',
	# 'ОКЕАН ЕЛЬЗИ','NAUTILIUS POMPILIUS','МУМИЙ ТРОЛЛЬ','МЕЛЬНИЦА','КУКРЫНИКСЫ','ЗВЕРИ','ЛЯПИС ТРУБЕЦКОЙ','THE BEATLES','НОЧНЫЕ СНАЙПЕРЫ',
	# 'RED HOT CHILI PEPPERS','PANIC AT THE DISCO','AC DC','SCORPIONS','NICKELBACK','АЛИСА','THREE DAYS GRACE','ЧАЙФ',
	# 'АКВАРИУМ','DEPECHE MODE','МАШИНА ВРЕМЕНИ','БРАВО','КНЯZZ','SKILLET','СМЫСЛОВЫЕ ГАЛЮЦИНАЦИИ','COLDPLAY','ТАНЦЫ МИНУС',
	# 'ПИЛОТ','Б','БУМБОКС','УРЕМАТОРИЙ','АНИМАЦИЯ','НЕРВЫ','LED ZIPPELIEN','EVANESCENCE','BON JOVI','PLACEBO','МУРАКАМИ','THE ROLLING STONES',
	# 'DEEP PURPLE','ELVIS PRESLEY','PINK FLOYD','ONE REPUBLIC','U','THE DOORS','AEROSMITH','НОГУ СВЕЛО','MAROON','СЕРЬГА',
	# 'LOBODA','РУКИ ВВЕРХ','ЕГОР КРИД','МАКС БАРСКИХ','ПОЛИНА ГАГАРИНА','SIA','ДИМА БИЛАН','ЕЛЕНА ТЕМНИКОВА','АНИ ЛОРАК',
	# 'BURITO','BEBE REXHA','SEREBRO','SHAKIRA','ЁЛКА','МАРИ КРАЙМБЕРИ','ED SHERAN','LANA DEL REY','ВРЕМЯ И СТЕКЛО','МАКСИМ','DUA LIPA',
	# 'MONATIC','MICHAEL JACKSON','ARIANA GRANDE','ХАННА','СЛАВА','НАРГИЗ','ГРАДУСЫ','BTS','НЮША','CRISTINA AGUILERA','SMASH',
	# 'CALVIN HARRIS','STING','LX','ПИЦЦА','ADELE','ALEKSEEV','ROBBIE WILLIAMS','ENRIQUE IGLASIAS','МАКС ФАДЕЕВ','IOWA',
	# 'KATY PARRY','JASTIN TIMBERLAKE','GRIVINA','ROXETTE','HURTS','ОЛЬГА БУЗОВА','ПОТАП И НАСТЯ','MALUMA','АРТЕМ ПИВОВАРОВ',
	# 'ТИМАТИ','МОНЕТОЧКА','GORILLAZ','TWENTY ONE PILOTS','RAGNBONE MAN','ALICE MERTON','THE XX','PORTUGAL THE MAN','ВАЛЕНТИН СТРЫКАЛО',
	# 'ДЕЛЬФИН','RADIOHED','МЫ','МАЛЬБЭК','TOM WALKER','FLORENCE','ГРЕЧКА','KALEO','ARCTIC MONKEYS','AJR','FLЁUR','DAMON ALBARN','ВАСЯ ОБЛОМОВ',
	# 'THE NEIGHBOURHOOD','ALTJ','ЛИНДА','KODALINE','THE KILLERS','MILKY CHANCE','HOZIER','АЛОЭВЕРА','ДАЙТЕ ТАНК','FOALS',
	# 'WOODKID','OH WINDER','SAINT MOTEL','LONDON GRAMMAR','PRAVADA','АИГЕЛ','СВИДАНИЕ','ZELLA DAY','THE KOOKS','GIN WIGMORE',
	# 'АРИЯ','LOUNA','METALLICA','SABATON','КИПЕЛОВ','NIGHTWISH','ЭПИДЕМИЯ','SLIPKNOT','POWERWOLF','WITHIN TEMPTATION','KORN',
	# 'OZZY OSBOURNE','BULLET FOR MY VALENTINE','IRON MAIDEN','APOCALYPTICA','GODSMACK','SYSTEM OF A DOWN','MANOWAR',
	# 'KORPIKLAANI','IN FLAMES','JUDAS PRIEST','STATIC X','ELEUVEITIE','EPICA','STONE SOUR','AMARANTHE','OOMPH','ROB ZOMBIE',
	# 'TRACKTOE BOWLING','FIVE FINGER DEATH PUNCH','KISS','BLACK SABBATH','STIGMATA','MEGADETH','ACCEPT','BLACK VEIL BRIDES',
	# 'AMATORY','EISBRECHER','LIMP BIZKIT','DROWNING POOL','HELLOWEEN','DEAD BY APRIL','VOLBEAT','SALIVA','LACUNA CIL','IN EXTREMO',
	# 'NINE INCH NAILS','PAIN','CHILDREN OF BODOM','NEMESEA','SLAYER','TRIVIUM','DOPE','POD','GHOST','PANTERA','DELAIN','DIO',
	# 'RAINBOW','LINKIN PARK','SYSTEM OF A DOWN','LUMEN','MUSE','NIRVANA','THIRTY SECONDS TO MARS','СЛОТ','FALL OUT BOY','MARLIN MANSON','THE WHITE STRIPES',
	# 'ANIMAL ДЖАZ','MIKE SHINODA','THOUSAND FOOT KRUTCH','THE RASMUS','DISTURBED','THE SCORE','KALEO','GREEN DAY','SUM',
	# 'GUANO APES','AWOLNATION','AVRIL LAVIGNE','LASCALA','KONGOS','GRANDSON','PAPA ROACH','HOLLYWOOD UNDEAD','THE PRETTY RECKLESS',
	# 'BRING ME THE HORIZON','REM','NOTHING BUT THEIVES','BREAKING BENJAMIN','MY CHEMICAL ROMANCE','KINGS OF LEON','M',
	# 'LIMP BIZKIT','PAME ON FIRE','PARAMORE','PARAMORE','ASKING ALEXANDIA','PIXIES','CRAZY TOWN','THE PRODIGY','MODY','DAFT PUK',
	# 'KYGO','PAROV STELAR','ATB','PENDULUM','SCOOTER','MARSHMELLO','MAJOR LAZER','MISSIO','THE AVENER','LINDSEY STIRLING',
	# 'MIA','MORCHEEBA','MASSIVE ATTACK','DANCE WITH THE DEAD','SKRILLEX','NERO','HIPPIE SABOTAGE','STROMAE','TONY IGY',
	# 'DIE ANTWOORD','ESCALE','THE CHEMICAL BROTHERS','DUKE DUMONT','MURA MASA','CLOZEE','THE GLITCH MOB','KAVINSKY','STEPHEN',
	# 'YELLO','PORTISHEAD','MUJUICE','JUNGLE','OFENBACH','BONZAI','DEEP HOUSE','MADONNA','DAVID GUETTA','CLEAN BANDIT',
	# 'GIGIDAGOSTINO','ARMIN VAN BUUREN','ARASH','НЕЙРОМОНАХ ФЕОФАН','MARTIN GARRIX','ROBIN SCHULZ','CALVIN HARRIS','SHOWTEK',
	# 'VANOTEK','ENELI','CBOOL','RUDIMENTAL','SHANGUY','AVICII','GIANG PHAM','PITBULL','DNCE','ALAN WALKER','INA WROLDSEN',
	# 'MAX OAZO','JAX JONSES','SIGALA','CAMI','ELDERBROOK','LP','SEAN PAUL','CAMELPHAT','TIMMY TRUMPET','THE CHAINSMOKERS',
	# 'SAM FELDT','MARI FERRARI','JAH KHALIB','БАСТА','NOIZE MC','MATRANGE','XXXTENTACION','МАКС КОРЖ','FEDUK','МОТ','LONE',
	# 'КРАЦ','КАСТА','ЛСП','ATL','ЗОМБ','MIAGI ЭНДШПИЛЬ','ГРОТ','РЕМ ДИГГА','TERRY','TFEST','СМОКИ МО','THOMAS MRAZ','NF',
	# 'OXXXYMIRON','PLC','PHARAOH','СКРИПТОНИТ','НОГГАНО','АНАСТАСИЯ АЛЕКСАНДРИНА','ЭЛДЖЕЙ','ДЖИГАН','MARKUL','МНОГОТОЧИЕ',
	# 'TKILLAH','FLO RIDA','ST','ГАНСЭЛЛО','СКРУДЖИ','ЧЕСТНЫЙ','AUBREY GRAHM','ГРИБЫ','KAMAZZ','ТРИАДА','TECH NNE','ХЛЕБ',
	# 'НИГАТИВ','КАРАНДАШ','IVAN VALEEV','NEFFEX','LEILA','SLIM','EMINEM','TARAS','ONYX','CENT','JUDAH','LOGIC','DOPE DOD',
	# 'SHAHMEN','KANYE WEST','WILEY','FORT MINOR','THE WEEKEND','RAY CHARLES','DENNIS LIOYD','SADE','THE BLACK EYED PEAS',
	# 'AMY WINEHOUSE','ALLAN RAYMAN','KWABS','NEYO','JACOB BANKS','WHITHEY HOUSTON','MANIA','KHALID','RIHANNA','FRANK OCEAN',
	# 'KIIARA','USHER','PRINCE','IMANY','FRANK SINATRA','RAY CHARLES','LOUIS ARMSTRONG','LOUNGE CAFE','NEW YORK JAZZ LOUNGE',
	# 'NORAH JONES','ELLA FITZGERALD','FAUSTO PAPETTI','NINA SIMONE','JAZZ LOUNGE','DAVE BRUBECK','KENNY G','PAUL DESMOND',
	# 'KAREN SOUZA','SMOOTH JAZZ','CHET BAKER','MILES DAVIS','CLARK TERRY','MICHEL BUBLE','PAPIK','STAN GETZ','MELODY GARDOT',
	# 'CHRIS REA','BUDDY GUY','ERIC CLAPTON','JOE BONAMASSA','NINA SIMONE','BETH HART','TOM WAITS','BILLYS BAND','HUGH LAUIRE',
	# 'BB KING','CREAM','SHAWN JAMES','FANTASTIC NEGRITO','ETTA JAMES','DUKE ROBILLARD','AL BASILE','ALANNH MYLES','JEFF BECK',
	# 'OTIS TAYLOR','FATS DOMINO','GARY MOORE','NIZZA','BOB MARLEY','THE WILERS','SHAGGY','ALAI OLI','STICK FIGURE','HADDAWAY',
	# 'МАРЛИНЫ','DUB FX','ALBOROSIE','INNER CIRCLE','BECKY G','MATISYAHU','REBELUTION','RASKAR','DAMIEN MARLEY','SHENSEEA',
	# 'FPG','NUMA CREW','TUFF STEPPAS','COMEDOZ','DON OMAR','THE HATTERS','DISTEMPER','ЛАМПАСЫ','TALCO','SKAP','RUSSKAJA',
	# 'ДОЗА РАДОСТИ','MALE FACTORS','КОРОЛЬ И ШУТ','ПОРНОФИЛЬМЫ','THE OFFSPRING','СЕКТОР ГАЗА','ТАРАКАНЫ','ГРАЖДАНСКАЯ ОБОРОНА',
	# 'ЭЛИЗИУМ','RISE AGAINST','GREEN DAY','НАИВ','SUM','BLINK','ПЛАН ЛОМОНОСОВА','ЙОРШ','КРАСНАЯ ПЛЕСЕНЬ','ЕГОР ЛЕТОВ',
	# 'NOFX','THE CLASH','VANILLA SKY','SLAVES','THE REAL MCKENZIES','ROMANES','LUSTRA','МИХАИЛ КРУГ','ИРИНА КРУГ',
	# 'СЕРГЕЙ ТРОФИМОВ','БУТЫРКА','АЛЕКСАНДР БРЯНЦЕВ','ЖЕКА','СЕРГЕЙ НАГОВИЦИН','ВИКТОР КОРОЛЕВ','ДЮМИН','АЛЕКСАНДР НОВИКОВ','ПЕТЛЮРА',
	# 'ГОЛУБЫЕ БЕРЕТЫ','МАФИК','АНТИРЕСПЕКТ','АНДРЕЙ БАНДЕРА','ПЯТИЛЕТКА','ЛЕСОПОВАЛ',''])""")

            # cur.execute("""SELECT musicbandid FROM public.musicband WHERE nameband LIKE ANY(array['ЛЕНИНГРАД','СПЛИН','IMAGINE DRAGONS','ЗЕМФИРА','QUEEN','AEROSMITH',
            #                                                                                      'LOBODA','ЕГОР КРИД','ПОЛИНА ГАГАРИНА','SIA','ED SHERAN','LANA DEL REY',
            #                                                                                      'МОНЕТОЧКА','GORILLAZ','TWENTY ONE PILOTS','RAGNBONE MAN','ALICE MERTON','THE XX',
            #                                                                                      'АЛОЭВЕРА','ДАЙТЕ ТАНК','FOALS','WOODKID','OH WINDER','SAINT MOTEL',
            #                                                                                      'SLIPKNOT','POWERWOLF','WITHIN TEMPTATION','KORN','OZZY OSBOURNE','BULLET FOR MY VALENTINE',
            #                                                                                      'RAINBOW','LINKIN PARK','SYSTEM OF A DOWN','LUMEN','MUSE','NIRVANA',
            #                                                                                      'REM','NOTHING BUT THEIVES','BREAKING BENJAMIN','MY CHEMICAL ROMANCE','KINGS OF LEON','M',
            #                                                                                      'LIMP BIZKIT','PAME ON FIRE','PARAMORE','PIXIES','THE PRODIGY','DIE ANTWOORD',
            #                                                                                      'TONY IGY','DEEP HOUSE','MADONNA','DAVID GUETTA','ARASH','НЕЙРОМОНАХ ФЕОФАН',
            #                                                                                      'JAH KHALIB','БАСТА','NOIZE MC','MATRANGE','FEDUK','МОТ',
            #                                                                                      'RIHANNA','KIIARA','USHER','FRANK SINATRA','RAY CHARLES','LOUIS ARMSTRONG',
            #                                                                                      'THE HATTERS','DISTEMPER','ЛАМПАСЫ','TALCO','SKAP','RUSSKAJA',
            #                                                                                      'GREEN DAY','SUM','BLINK','ПЛАН ЛОМОНОСОВА','ЙОРШ','КРАСНАЯ ПЛЕСЕНЬ',
            #                                                                                      'МИХАИЛ КРУГ','ИРИНА КРУГ','СЕРГЕЙ ТРОФИМОВ','БУТЫРКА','АЛЕКСАНДР БРЯНЦЕВ','ЖЕКА'])""")
            musicband = cur.fetchall()
            print(musicband)
            with open('files/musicbanddump.pkl', 'wb') as output_file:
                pickle.dump(musicband, output_file)
        else:
            with open('files/musicbanddump.pkl', 'rb') as output_file:
                musicband = pickle.load(output_file)
    except:
        print('Сломалася')
    svaz = [[5587], [5588]]
    listDrop = []
    print("START")
    # +1 для замены последнего значения на выбранную специальность
    dfaALL = np.zeros((len(musicband)+1,), dtype=np.uint8)
    dfaUser = np.zeros((len(users)), dtype=np.uint32)
    for indexU, j in enumerate(users):
        dfa = np.zeros((len(musicband) + 1), dtype=np.uint8)
        try:
            cur.execute("SELECT idclear FROM vkuser_clearmusicbandnew WHERE idvkuser = "+str(j[0])+" order by idclear")
            svaz = cur.fetchall()
            print(svaz)
        except:
            print("запрос списка связи упал")
        try:
            cur.execute("SELECT f.category FROM vkuser as v INNER JOIN faculty as f ON f.facultyid = v.faculty WHERE uservkid = "+str(j[0])+"")
            category = cur.fetchall()

        except:
            print("запрос списка связи упал")
        print(indexU, "< USER")
        summaDrop = 0
        for indexS, k in enumerate(svaz):
            try:
                if musicband.index(k) != 0:
                    print(musicband.index(k), "----------------------------------")
                    dfa[musicband.index(k)] = 1
                    summaDrop+=1
                    print(summaDrop,' ---------================--=-=-=-=-=-=====')
            except ValueError as e:
                print("ERROR > ", e)
        if summaDrop == 0:
            print("НУЛИ//////////////////////////////////////////////////////////////////")
            continue
        dfa[len(musicband)] = category[0][0]
        print(j[0])
        dfaUser[indexU] = j[0]
        # print(dfaUser)
        # print("ТАБЛИЦА\n", dfaALL)
        dfaau = pd.DataFrame(dfaUser)

        # print(dfaau)
        # dfaALL = numpy.vstack((dfaALL, dfa))
        # dfaa = pd.DataFrame(dfaALL)
        # print(dfaa)

        # dfaO = np.zeros((len(musicband) + 1), dtype=np.uint8)
        # dfaO = np.vstack((dfaO, dfa))
        #
        # dfaOut = pd.DataFrame(dfaO)
        # #print(dfaOut)

        print(dfa)
        dfa = np.expand_dims(dfa, axis=0)
        print(dfa.shape, "=======",len(dfa))
        # np.savetxt('files/output6.txt', dfa, delimiter=',')
        dfaOut = pd.DataFrame(dfa)

        @contextmanager
        def open_file(path, mode):
            file_to = open(path, mode)
            yield file_to
            file_to.close()

        try:
            print("ЗАПИСЬ", indexU)
            if categ == 0:

                with open_file('files/output12.csv', 'r') as infile:
                    dfaOut.to_csv('files/output12.csv', mode='a', header=False)

                dfaau.to_csv('files/output6User.csv')
                print("ЗАПИСАНО")
                # f.close()
            else:
                dfaau.to_csv('files/output1User.csv')
                dfaOut.to_csv('files/output1.csv', mode='a')
                print("ЗАПИСАНО 1")
        except:
            print("Упала запись в файл")




def treeLearn(param, trees):
    if param == True:
        # df = pd.read_csv('files/output6.csv', dtype='uint32', low_memory=False)

        # dfaUser = np.zeros((195000, 2500), dtype=np.uint32)
        # print(dfaUser)
        # df = np.memmap('files/output6.csv', dtype='uint32', mode='r')
        # print(df)
        c1=0
        c2=0
        # c3=0
        # c4=0
        # c5=0
        # mylist = np.array([])
        # with open("files/output12.csv", "r") as f:
        #     reader = csv.reader(f)
        #     for i, line in enumerate(reader):
        #         print(line[len(line)-1])
        #         print(c1, c2)
        #         if line[len(line)-1]=='1':
        #             if c1 != 500:
        #                 c1+=1
        #                 mylist = np.vstack((mylist, line))
        #         elif line[len(line)-1]=='2':
        #             if c2 != 500:
        #                 c2+=1
        #                 mylist = np.vstack((mylist, line))
        #         print(mylist,'my list===================================')

        mylist = []
        for chunk in pd.read_csv('files/output12.csv', chunksize=100, dtype='uint32', low_memory=False):
            mylist.append(chunk)
            print(mylist)


        df = pd.concat(mylist, axis=0)
        print(df)
        del mylist
        # print(df.sum(axis=1))

        ndf = df.as_matrix()
        print(ndf)
        n = np.sum(ndf[:,:-1],axis=1)
        print(np.sum(ndf[:,:-1],axis=1))
        deletSum = []
        for index, o in enumerate(n):
            if o < 10:
                print(o)
                deletSum.append(index)
        print(deletSum,'delsum')
        ndf = np.delete(ndf, deletSum, axis=0)
        print(ndf, ndf.shape)
        deletSum.clear()
        c1 = 0
        c2 = 0
        c11 = 0
        c22 = 0
        np.random.shuffle(ndf)
        print(ndf)
        catdf = ndf[:, ndf.shape[1] - 1]
        print(catdf)
        for index, o in enumerate(catdf):
            if o == 1:
                if c11 != 442:
                    c1+=1
                    c11+=1
                else:
                    deletSum.append(index)
            else:
                if c22 != 442:
                    c2+=1
                    c22+=1
                else:
                    deletSum.append(index)
        print(deletSum)
        ndf = np.delete(ndf, deletSum, axis=0)
        print(ndf, ndf.shape)
        print(c1,c2)

        dfa = pd.DataFrame(ndf)

        # print(df.shape,'shape')
        # print(df.iloc[0], 'iloc')
        # print(df.iloc[1], 'iloc')
        # print(df.index[0],'index')

        q = len(df.columns) - 1
        print(q)
        df = df.astype(int)
        print("РОБИТ?\n", df)
        X = df.values[:, 1:q]
        Y = df.values[:, q]
        print(X, "<<<<<<<<<<<<<<X")
        print(Y, "<<<<<<<<<<<<<<Y")




        tree_params = {'max_depth': range(2, 31),'max_features': range(4, 30), 'min_samples_leaf': range(1, 30)}
        tree_grid = GridSearchCV(trees, tree_params,cv=4, n_jobs=5)


        kf = KFold(n_splits=5,shuffle=True)
        print(kf.get_n_splits(X))
        for train_index, test_index in kf.split(X):
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = X[train_index], X[test_index]
            Y_train, Y_test = Y[train_index], Y[test_index]

        # tree_grid.fit(X_train, Y_train)
        # print(tree_grid.best_params_, '<<параметры ', tree_grid.best_score_, " <<лучшее значение")

        trees.fit(X_train, Y_train)
        print(trees.score(X_test,Y_test)," <<<<<<<<<<<< точность совпадений")

        # trees_pred = tree_grid.predict(X_test)
        #
        # print(accuracy_score(Y_test, trees_pred), ">>>>>>>>>>>>>>> точность")
        # print(f1_score(Y_test, trees_pred, average='weighted'), ">>>>>>>>>>>>>>> точность weighted")
        # print(f1_score(Y_test, trees_pred, average=None), ">>>>>>>>>>>>>>> точность weighted")
        # print(recall_score(Y_test, trees_pred, average='weighted'), ">>>>>>>>>>>>>>> точность recall_score")
        # print(recall_score(Y_test, trees_pred, average=None), ">>>>>>>>>>>>>>> точность recall_score")
        # print(precision_score(Y_test, trees_pred, average='weighted'), ">>>>>>>>>>>>>>> точность precision_score")
        # print(precision_score(Y_test, trees_pred, average=None), ">>>>>>>>>>>>>>> точность precision_score")
        # print()

        tree_pred = trees.predict(X_test)
        print(accuracy_score(Y_test, tree_pred), ">>>>>>>>>>>>>>> точность")
        print(f1_score(Y_test, tree_pred, average='weighted'), ">>>>>>>>>>>>>>> точность weighted")
        print(f1_score(Y_test, tree_pred, average=None), ">>>>>>>>>>>>>>> точность weighted")
        print(recall_score(Y_test, tree_pred, average='weighted'), ">>>>>>>>>>>>>>> точность recall_score")
        print(recall_score(Y_test, tree_pred, average=None), ">>>>>>>>>>>>>>> точность recall_score")
        print(precision_score(Y_test, tree_pred, average='weighted'), ">>>>>>>>>>>>>>> точность precision_score")
        print(precision_score(Y_test, tree_pred, average=None), ">>>>>>>>>>>>>>> точность precision_score")

        with open('files/treesdump.pkl', 'wb') as output_file:
            pickle.dump(trees, output_file)
        # X_train, X_holdout, Y_train, Y_holdout = train_test_split(df.values, Y, test_size=0.3, random_state=17)
        # trees.fit(X_train, Y_train)
        # tree_pred = trees.predict(X_holdout)
        # accuracy_score(Y_holdout, tree_pred)
        # print(accuracy_score(Y_holdout, tree_pred))
        print("------------------------------------------------------------------------")
        #рисование дерева
        try:
            dot_data = tree.export_graphviz(trees, out_file=None, rounded=True, filled=True)
            graph = pydotplus.graph_from_dot_data(dot_data)
            graph = graphviz.Source(dot_data)
            graph.render("files/iris")
        except:
            print("рисование дерево не получилось")




    else:
        with open('files/treesdump.pkl', 'rb') as output_file:
            trees1 = pickle.load(output_file)
        df = pd.read_csv('files/output2.csv', dtype='uint32', low_memory=False)
        q = len(df.columns) - 1
        print(q)
        df = df.astype(int)
        print("РОБИТ?\n", df)
        X = df.values[:, 1:q]
        Y = df.values[:, q]
        print(X, "<<<<<<<<<<<<<<X")
        print(Y, "<<<<<<<<<<<<<<Y")
        trees1.predict(X)
        print(trees1.predict(X), "------------------ пробуем")

# tableLearn(0)

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
                'ФИЗИЧЕСКОЙ') > -1 or j[1].find('РУССК') > -1 or j[1].find('ЛИТЕРАТ') > -1 or j[1].find('МЕНЕДЖ') > -1 or j[1].find('ФИНАН') > -1 or j[1].find('ЭКОНОМ') > -1 or j[1].find('ПРАВО') > -1 or j[1].find('ЮРИД') > -1 or j[1].find('ПРАВА') > -1 or j[1].find(
                    'АРБИТ') > -1 or j[1].find('АДВОКА') > -1 or j[1].find('УГОЛОВ') > -1 or j[1].find(
                'ФИЛОС') > -1 or j[1].find('ИСТОР') > -1 or j[1].find('ЮРИС') > -1:
                print(j[1], "<========Гуманитарный")
                cur.execute("UPDATE faculty SET category = '1' WHERE facultyid ='" + str(j[0]) + "'")


            elif j[1].find('БИОЛ') > -1 or j[1].find('ЕСТЕСТ') > -1 or j[1].find('ГЕОЛ') > -1 or j[1].find(
                    'НЕФТ') > -1 or j[1].find('ГАЗА') > -1 or j[1].find('БУРЕ') > -1 or j[1].find('АВТОМ') > -1 or \
                    j[1].find('ХИМИ') > -1 or j[1].find('ЭКОЛО') > -1 or j[1].find('ПРИРОДО') > -1 or j[1].find(
                'ЭНЕРГЕ') > -1 or j[1].find('НЕФТЕ') > -1 or j[1].find('МАТЕМ') > -1 or j[1].find('ТЕХН') > -1 or j[1].find('ЭЛЕКТ') > -1 or j[1].find(
                    'СИСТЕМ') > -1 or j[1].find('ВЫЧИСЛИ') > -1 or j[1].find('ИНЖЕН') > -1 or j[1].find(
                'ИНФОРМ') > -1 or j[1].find('МОДЕЛИ') > -1 or j[1].find('СТРОИТ') > -1 or j[1].find(
                'ФИЗИК') > -1 or j[1].find('ТЕХНИЧ') > -1 or j[1].find('ТЕХНОЛОГ') > -1 or j[1].find('ТРАНСПОРТ') > -1:
                print(j[1], "<========Техники")
                cur.execute("UPDATE faculty SET category = '2' WHERE facultyid ='" + str(j[0]) + "'")
            else:
                print('Неизвестное сочетание')
                cur.execute("UPDATE faculty SET category = '0' WHERE facultyid ='" + str(j[0]) + "'")
        conn.commit()
    except:
        print("факультет упал")

try:
    conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
    print("connect OK")
except:
    print("Не удалось подключиться к БД")
# Создаем курсор для работы
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def main():
    # запрос на апдейт факультетеов
    try:
        cur.execute("SELECT facultyid, name FROM faculty ORDER BY name")
        results = cur.fetchall()
        print(results)
        categoryFaculty(results)
    except psycopg2.DatabaseError as e:
        if conn:
            conn.rollback()
        print('Error %s' % e)
        print("ЧТО то пошло не так")

    # tableLearn(0)
    trees = tree.DecisionTreeClassifier(max_depth=30)
    treeLearn(True, trees)

# with open('files/treesdump.pkl', 'rb') as output_file:
#     trees1 = pickle.load(output_file)
# df = pd.read_csv('files/output2.csv')
# q = len(df.columns) - 1
# print(q)
# df = df.astype(int)
# print("РОБИТ?\n", df)
# X = df.values[:, 1:q]
# Y = df.values[:, q]
# print(X, "<<<<<<<<<<<<<<X")
# print(Y, "<<<<<<<<<<<<<<Y")
# trees1.predict(X)
# print(trees1.predict(X),"------------------ пробуем")






#
# df = pd.read_csv('iris_df.csv')
# #df.columns = ['X1', 'X2', 'X3', 'X4', 'Y']
# #df.head()
# print(df)
# print("HEAD")
#
# q = len(df.columns)-1
# print(q)
#
# df=df.astype(int)
# print("РОБИТ?\n",df)
#
# X = df.values[:, 0:q]
# Y = df.values[:, q]
# print(X,"<<<<<<<<<<<<<<X")
# print(Y,"<<<<<<<<<<<<<<Y")
#
# X_train, X_holdout, Y_train, Y_holdout = train_test_split(df.values, Y, test_size=0.3,
# random_state=17)
#
# tree = tree.DecisionTreeClassifier(max_depth=5, random_state=17)
#
#
# #clf = tree.DecisionTreeClassifier()
# tree.fit(X_train, Y_train)
# tree_pred = tree.predict(X_holdout)
# accuracy_score(Y_holdout, tree_pred)
# print(accuracy_score(Y_holdout, tree_pred))
# print("------------------------------------------------------------------------")
#
#
#
#
# # clf = clf.fit(X, Y)
# #
# # print(clf.predict([[7.6,5.1,1.4,0.2,1]]),'<<<<<<<<<<<предсказание')
# # print(clf.predict_proba([[4.3,3.9,1.5,0.2,2]]),'<<<<<<<<<<<предсказание')
# # print(clf.predict([[4.3,3.9,1.5,0.2,2]]),'<<<<<<<<<<<предсказание')
# #
# # dot_data = tree.export_graphviz(clf, out_file=None, rounded=True, filled=True)
# # graph = pydotplus.graph_from_dot_data(dot_data)
# # graph = graphviz.Source(dot_data)
# # graph.render("files/iris")
# #
# #
# # print('finish')
# #
# # plt.subplot(1,1,1)
# # plt.axis("tight")
# # plt.show()

if __name__ == '__main__':
    main()