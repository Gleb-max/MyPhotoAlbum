import os
from flask import Flask, request, render_template, send_from_directory
from werkzeug.utils import secure_filename


app = Flask(__name__)
INDEX = 1


def image_path(name):
    global INDEX
    name = secure_filename(name)
    if len(name.split('.')) == 1:
        name = f'{INDEX}.{name}'
        INDEX += 1
    return f'Images/{name}'


@app.route('/show/images/')
def show_images():
    return render_template('show-image.html', names=os.listdir('Images'))


@app.route('/add/images/', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        file = request.files['photo']
        file.save(image_path(file.filename))
        return render_template('show-image.html', names=os.listdir('Images'))
    return render_template('upload-image.html')


@app.route('/open/<filename>')
def open_image(filename):
    return send_from_directory('Images', filename)


if __name__ == '__main__':
    app.run()
