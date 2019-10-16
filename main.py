import io
import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
from threading import Thread


app = Flask(__name__)
INDEX = 1
IMAGE_FOLDER = 'Images/'
MINIATURES_FOLDER = 'Miniatures/'


def image_name(name):
    global INDEX
    name = secure_filename(name)
    if len(name.split('.')) == 1:
        name = f'{INDEX}.{name}'
        INDEX += 1
    return name


def create_miniature(filename):
    Image.open(IMAGE_FOLDER + filename).resize((100, 100), Image.ADAPTIVE).save(MINIATURES_FOLDER + filename)


@app.route('/show/images/')
def show_images():
    return render_template('show-image.html', names=os.listdir('Miniatures'))


@app.route('/add/images/', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        file = request.files['photo']
        filename = image_name(file.filename)
        file.save(IMAGE_FOLDER + filename)
        Thread(target=lambda: create_miniature(filename)).start()
        return render_template('show-image.html', names=os.listdir('Miniatures'))
    return render_template('upload-image.html')


@app.route('/open/<directory>/<filename>')
def open_image(directory, filename):
    return send_from_directory(directory, filename)


if __name__ == '__main__':
    app.run()
