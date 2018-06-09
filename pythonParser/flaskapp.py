import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import json
import vksearch
app = Flask(__name__)


@app.route("/")
@app.route("/index")
def hello():
    return render_template("home.html", massage = 'Добро пожаловать!')

UPLOAD_FOLDER = r'D:\uploadfile'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#допустимые расширения файлов
ALLOWED_EXTENSIONS = set(['json'])
#функция проверки файлов
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
                vksearch.program(audio)
            except Exception as e:
                print(e)
                print('Загрузка файла не удалась')
                f.close()
                return render_template("home.html", massage='Загрузка файла провалилась')
    except:
        f = None
        print('лажа')
        return render_template("home.html", massage = 'Загрузка файла провалилась')









if __name__ == "__main__":
    app.run()