from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CDMM import Command, User, connect
import hashlib
from wtforms.validators import InputRequired, Length
from flask_session import Session
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user

# Создаем приложение Flask
app = Flask(__name__)

# Устанавливаем соединение с базой данных
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = '25n23j5b2jh5v23jh5v24j5v2hj45'  # Задайте свой секретный ключ для сессий
# Создаем таблицы, если они еще не созданы
connect('sqlite:///example.db')



# Путь к папке для загрузки изображений
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Создайте папку для загрузки, если она не существует
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Список для хранения данных о загруженных изображениях
images_data = []

class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.username

    def is_active(self):
        return True

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        return False

def calculate_file_hash(file_path):
    """Вычисляет хэш-сумму файла по указанному пути с использованием заданного алгоритма."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл '{file_path}' не существует.")

    # Открываем файл для бинарного чтения
    with open(file_path, 'rb') as f:

        hash_obj = hashlib.md5()

        # Читаем файл блоками и обновляем хэш-объект
        while True:
            data = f.read(65536)  # Читаем блок размером 64 Кбайт
            if not data:
                break
            hash_obj.update(data)

    # Возвращаем строковое представление хэш-суммы
    return hash_obj.hexdigest()
def rename_file_to_hash(file_path):
    """Переименовывает файл по указанному пути в его хэш-сумму."""

    # Вычисляем хэш-сумму файла
    file_hash = calculate_file_hash(file_path)

    # Получаем имя файла без пути
    file_name = os.path.basename(file_path)

    # Формируем новое имя файла из хэш-суммы
    new_file_name = f"{file_hash}.{file_name}"

    # Переименовываем файл
    os.rename(file_path, os.path.join(os.path.dirname(file_path), new_file_name))

    return new_file_name

@login_manager.user_loader
def load_user(username):
    # Query and return user from the database
    command = session.query(Command).filter_by(username=username).first()
    if command:
        return User(command.username, command.password)
    return None

@app.route('/')
def index():
    # Отображаем главную страницу со списком изображений
    return render_template('index.html', images_data=images_data)


# логин и регистрация
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return f'Вы уже вли в аккаунт: {current_user.username}'
    if request.method == 'POST':
        # Получаем данные из формы
        team_name = request.form['team_name']
        team_photo = request.files['team_photo']
        email = request.form['email']
        about = request.form['about']
        username = request.form['username']
        password1 = request.form['password1']
        password2 = request.form['password2']
        
        # Сравниваем пароли
        if password1!=password2:
            return "Ведёные пароли не совпадают"

        # Сохраняем изображение в папку для загрузок
        # ДОБАВИТЬ ИЗМЕНЕНИЕ ИМЕНИ НА ХЕШ СУММУ
        if team_photo.filename.endswith(('png', 'jpg', 'jpeg')):
            filename = team_photo.filename
            team_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Добавляем оманду в базу данных
        command = Command(team_name=team_name, image=filename, team_info=about, email=email, username=username, password=password1)
        try:
            session.add_all([command])
            session.commit()
            return redirect(url_for('login'))
        except Exception as ex:
            print(ex)
            return "Проиошла оибка"
            
            # Перенаправляем пользователя на главную страницу
            
    return render_template('reg.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return f'Вы уже вли в аккаунт: {current_user.username}'
    if request.method == 'POST':
            command = session.query(Command).filter_by(username=request.form["username"]).first()
            if not command:
               return "Команда с таким логиином не найдена" 
            if command.password!=request.form["password"]:
                return "Введён не правильный пароль"
            user = User(request.form['username'], request.form['password'])
            login_user(user)
            return redirect(url_for('dashboard'))
            
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        return f'Hello, {current_user.username}! This is the dashboard.'
    else:
        return 'User not authenticated'

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'You are logged out'


# Запускаем приложение Flask
if __name__ == '__main__':
    app.run(debug=True)



