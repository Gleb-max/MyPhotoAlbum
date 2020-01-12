from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from threading import Thread
from PIL import Image
import os


app = Flask(__name__)
INDEX = 0
IMAGE_FOLDER = 'img/'
MINIATURES_FOLDER = 'min/'


def image_name(name):    # возвращает безопасное имя для загружаемой картинки
    global INDEX         # функция secure_filename возвращает только расширение файла
    name = secure_filename(name)    # в случае "опасности" имени,
    data = name.split('.')          # поэтому такие картинки сохраняю под числовым именем,
    if len(data) == 1:              # попутно следя, чтобы картинки не "пересохранялись"
        name = f'{INDEX}.{name}'    # (в случае числового имени загружаемой картинки)
        INDEX += 1
    elif len(data) == 2 and data[0].isdigit():
        name = f'{INDEX}.{data[1]}'
        INDEX += 1
    return name


def create_miniature(filename):     # создание миниатюры
    Image.open(IMAGE_FOLDER + filename).resize((500, 500), Image.ADAPTIVE).save(MINIATURES_FOLDER + filename)


@app.route('/gallery/', methods=['GET', 'POST'])    # единственная страница (на ней и галерея и загрузка)
def show_images():
    if request.method == 'POST':
        global INDEX
        INDEX += 1
        file = request.files['photo']
        #filename = image_name(file.filename)
        filename = str(INDEX) + ".png"
        file.save(IMAGE_FOLDER + filename)
        Thread(target=lambda: create_miniature(filename)).start()   # создание миниатюры в отдельном потоке
    return render_template('show-image.html', names=os.listdir('min'))  # для ускорения ответа


@app.route('/open/<directory>/<filename>')   # открытие файла, указанного в пути <directory>/<filename>
def open_file(directory, filename):
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run()
