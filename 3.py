import os
from flask import Flask, request, render_template
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/show/images/')
def show_images():
    return render_template('show-image.html', names=os.listdir('Images'))


@app.route('/add/images/', methods=['GET', 'POST'])
def add_image():
    if request.method == 'POST':
        file = request.files['photo']
        file.save('Images/' + secure_filename(file.filename))
        return 'Successfully'
    return render_template('upload-image.html')


if __name__ == '__main__':
    app.run()
