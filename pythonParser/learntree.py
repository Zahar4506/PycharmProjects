
import pandas as pd
import numpy
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
from sklearn.metrics import accuracy_score
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
        cur.execute("SELECT idmusicbandnew FROM newmusicband order by idmusicbandnew")
        musicband = cur.fetchall()
        print(musicband)
    except:
        print('Сломалася')
    svaz = [[5587], [5588]]
    print("START")
    # +1 для замены последнего значения на выбранную специальность
    dfaALL = numpy.zeros((len(musicband)+1), dtype=numpy.uint8)
    dfaUser = numpy.zeros((len(users)), dtype=numpy.uint32)
    for indexU, j in enumerate(users):
        dfa = numpy.zeros((len(musicband) + 1), dtype=numpy.uint8)
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

        for indexS, k in enumerate(svaz):
            try:
                if musicband.index(k) != 0:
                    print(musicband.index(k), "----------------------------------")
                    dfa[musicband.index(k)] = 1
            except ValueError as e:
                print("ERROR > ", e)


        # for indexM, i in enumerate(musicband):
        #     for indexS, k in enumerate(svaz):
        #         try:
        #             print(musicband.index(k[0]))
        #             if musicband.index(k[0])!=0:
        #                 print("----------------------------------")
        #                 dfa[indexM] = 1
        #             break
        #         except ValueError as e:
        #             print("ERROR > ",e)

        dfa[len(musicband)] = category[0][0]
        print(j[0])
        dfaUser[indexU] = j[0]
        print(dfaUser)
        print("ТАБЛИЦА\n", dfaALL)
        dfaau = pd.DataFrame(dfaUser)
        print(dfaau)
        dfaALL = numpy.vstack((dfaALL, dfa))
        dfaa = pd.DataFrame(dfaALL)
        print(dfaa)
        time.sleep(1)
        try:
            print("ЗАПИСЬ")
            if categ == 0:
                dfaau.to_csv('files/output5User.csv')
                dfaa.to_csv('files/output5.csv')
                print("ЗАПИСАНО")
            else:
                dfaau.to_csv('files/output1User.csv')
                dfaa.to_csv('files/output1.csv')
                print("ЗАПИСАНО 1")
        except:
            print("Упала запись в файл")
        time.sleep(1)



def treeLearn(param, trees):
    if param == True:
        df = pd.read_csv('files/output2.csv')
        q = len(df.columns) - 1
        print(q)
        df = df.astype(int)
        print("РОБИТ?\n", df)
        X = df.values[:, 1:q]
        Y = df.values[:, q]
        print(X, "<<<<<<<<<<<<<<X")
        print(Y, "<<<<<<<<<<<<<<Y")
        kf = KFold(n_splits=2)
        kf.get_n_splits(X)
        print(kf.get_n_splits(X))
        for train_index, test_index in kf.split(X):
            print("TRAIN:", train_index, "TEST:", test_index)
            X_train, X_test = X[train_index], X[test_index]
            Y_train, Y_test = Y[train_index], Y[test_index]
        trees.fit(X_train, Y_train)
        trees.score(X_test,Y_test)
        print(trees.score(X_test,Y_test)," <<<<<<<<<<<< точность совпадений")

        tree_pred = trees.predict(X_test)
        accuracy_score(Y_test, tree_pred)
        print(accuracy_score(Y_test, tree_pred), ">>>>>>>>>>>>>>> точность")

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
        df = pd.read_csv('files/output2.csv')
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

tableLearn(0)

# trees = tree.DecisionTreeClassifier(max_depth=15, random_state=17)
# treeLearn(True, trees)
#
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