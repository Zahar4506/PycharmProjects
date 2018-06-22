
import pandas as pd
import numpy
import warnings

import matplotlib.pyplot as plt
import psycopg2
import psycopg2.extras
import pydotplus

warnings.filterwarnings("ignore")

from sklearn import tree

import graphviz
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score
from sklearn.model_selection import GridSearchCV, cross_val_score

try:
    conn = psycopg2.connect("dbname='vk' user='postgres' host='127.0.0.1' password='1'")
    print("connect OK")
except:
    print("Не удалось подключиться к БД")
# Создаем курсор для работы
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
try:
    cur.execute("SELECT uservkid FROM vkuser order by uservkid LIMIT 50")
    users = cur.fetchall()
    print(users)
    cur.execute("SELECT idmusicbandnew FROM newmusicband order by idmusicbandnew LIMIT 50")
    musicband = cur.fetchall()
    print(musicband)
except:
    print('Сломалася')
svaz = [[5587], [5588]]
print("START")
dfa = numpy.zeros((len(musicband),len(users)),dtype=numpy.int)
for indexU, j in enumerate(users):

    cur.execute("SELECT idclear FROM vkuser_clearmusicbandnew WHERE idvkuser = "+str(j[0])+" order by idclear")
    svaz = cur.fetchall()
    print(svaz)

    for indexM, i in enumerate(musicband):
        for indexS, k in enumerate(svaz):
            try:
                print(k[0], " < k")
                print(i, " < i")
                print(i.index(k[0]))
                print(indexU," ",indexM, " ", indexS)
                if i.index(k[0])==0:
                    print("----------------------------------")
                    dfa[indexU][indexM] = 1
                break
            except ValueError as e:
                print("ERROR > ",e,"\n")

print("ТАБЛИЦА\n",dfa)
dfaa = pd.DataFrame(dfa)
print(dfaa)
dfaa.to_csv('files/output.csv')


df = pd.read_csv('iris_df.csv')
#df.columns = ['X1', 'X2', 'X3', 'X4', 'Y']
#df.head()
print(df)
print("HEAD")

q = len(df.columns)-1
print(q)

df=df.astype(int)
print("РОБИТ?\n",df)

X = df.values[:, 0:q]
Y = df.values[:, q]
print(X,"<<<<<<<<<<<<<<X")
print(Y,"<<<<<<<<<<<<<<Y")

X_train, X_holdout, Y_train, Y_holdout = train_test_split(df.values, Y, test_size=0.3,
random_state=17)

tree = tree.DecisionTreeClassifier(max_depth=5, random_state=17)


#clf = tree.DecisionTreeClassifier()
tree.fit(X_train, Y_train)
tree_pred = tree.predict(X_holdout)
accuracy_score(Y_holdout, tree_pred)
print(accuracy_score(Y_holdout, tree_pred))
print("------------------------------------------------------------------------")




# clf = clf.fit(X, Y)
#
# print(clf.predict([[7.6,5.1,1.4,0.2,1]]),'<<<<<<<<<<<предсказание')
# print(clf.predict_proba([[4.3,3.9,1.5,0.2,2]]),'<<<<<<<<<<<предсказание')
# print(clf.predict([[4.3,3.9,1.5,0.2,2]]),'<<<<<<<<<<<предсказание')
#
# dot_data = tree.export_graphviz(clf, out_file=None, rounded=True, filled=True)
# graph = pydotplus.graph_from_dot_data(dot_data)
# graph = graphviz.Source(dot_data)
# graph.render("files/iris")
#
#
# print('finish')
#
# plt.subplot(1,1,1)
# plt.axis("tight")
# plt.show()