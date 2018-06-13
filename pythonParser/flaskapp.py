import os
import subprocess
from concurrent.futures import ThreadPoolExecutor

from flask import Flask, render_template, request
from multiprocessing import Process
from werkzeug.utils import secure_filename
import json
import vksearch
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def hello():
    return render_template("home.html", massage = 'Добро пожаловать!')\

@app.route("/about")
def about():
    return render_template("about.html", massage = 'Добро пожаловать!')

UPLOAD_FOLDER = r'D:\uploadfile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#допустимые расширения файлов
ALLOWED_EXTENSIONS = set(['json'])
#функция проверки файлов
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/search")
def search():
    return render_template("search.html", massage='asdasd')

def pup(audio):
    subprocess.Popen(vksearch.program(audio))

@app.route("/uploadfile/", methods=['POST'])
def upload_file():
    try:
        if request.method == 'POST':
            f = request.files['filename']
            print(allowed_file(f.filename), '<<<<')
            print(f and allowed_file(f.filename), '>>>>>')
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                print('работает')
                print(filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            else:
                return render_template("home.html", massage = 'Неверное расширение файла')
            try:
                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r', encoding='utf-8') as f:
                    str = f.read()
                    print(json.dumps(str))
                    print(json.loads(str))
                    audio = json.loads(str)
                    print(str)
                    print(audio)
                    f.close()
                print('START')

                #pup(audio)

                with ThreadPoolExecutor(max_workers=2) as executor:
                    executor.submit(vksearch.program(audio), ())

                # p = Process(target=vksearch.program(audio))
                # p.start()
                # p.join()

                return render_template("search.html", massage='Расчеты произведены!')

            except Exception as e:
                print(e, ' <<<<<error')
                print('Загрузка файла не удалась')
                f.close()
                return render_template("home.html", massage='Загрузка файла провалилась')
    except:
        f = None
        print('лажа')
        return render_template("home.html", massage = 'Загрузка файла провалилась')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', massage = "Ошибка 404, страница не найдена"), 404

@app.errorhandler(500)
def internal_error(e):
    return render_template('500.html', massage = "Непредвиденная ошибка на сервере"), 500





if __name__ == "__main__":
    app.debug = True
    app.run()