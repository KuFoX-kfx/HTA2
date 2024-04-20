from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os

app = Flask(__name__)

# Путь к папке для загрузки изображений
UPLOAD_FOLDER = 'static/photos'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создайте папку для загрузки, если она не существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Список для хранения данных о загруженных изображениях
images_data = []

@app.route('/')
def index():
    # Отображаем главную страницу со списком изображений
    return render_template('index.html', images_data=images_data)





if __name__ == '__main__': app.run(debug=True)


from flask import Flask, jsonify

app =Flask(__name__)
data = {
    'images':[
        {
            'id': 1,
            'filename': 'image1.jpg',
            'description': 'Image 2 description'
        },
    ]
}

@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(data)
if __name__ == '__main__':
    app.run(debug=True)