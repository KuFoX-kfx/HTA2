from flask import Flask, render_template, request, redirect, url_for, session
from PIL import Image
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CDMM import Command, User, connect
from hashlib import md5
import hashlib
from wtforms.validators import InputRequired, Length
from flask_session import Session
from werkzeug.utils import secure_filename
from flask_login import current_user, LoginManager, UserMixin, login_user, login_required, logout_user

# Заглушка для данных команды
team_data = {
    'team_name': 'Моя команда',
    'team_info': 'Описание моей команды',
    'team_members': 'Участник 1\nУчастник 2\nУчастник 3',
    'profile_image': 'default-profile.png'
}

# Создаем приложение Flask
app = Flask(__name__)

# Устанавливаем соединение с базой данных
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = '25n23j5b2jh5v23jh5v24j5v2hj45'  # Задайте свой секретный ключ для сессий
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
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


    
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Модель данных для пользователей


    

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
# def rename_file_to_hash(file_path):
#     """Переименовывает файл по указанному пути в его хэш-сумму."""

#     # Вычисляем хэш-сумму файла
#     file_hash = calculate_file_hash(file_path)

#     # Получаем имя файла и расширение
#     file_name, file_extension = os.path.splitext(os.path.basename(file_path))

#     # Формируем новое имя файла из хэш-суммы и оригинального расширения
#     new_file_name = f"{file_hash}{file_extension}"

#     # Получаем путь к директории файла
#     file_directory = os.path.dirname(file_path)

#     # Формируем полный путь к новому имени файла
#     new_file_path = os.path.join(file_directory, new_file_name)

#     # Переименовываем файл
#     try:
#         os.rename(file_path, new_file_path)
#     except:
#         pass

#     return new_file_name

# @login_manager.user_loader
# def load_user(username):
#     # Query and return user from the database
#     command = session.query(Command).filter_by(username=username).first()
#     if command:
#         return Command(command.username, command.password)
#     return None
def rename_file_to_hash(file_path):
    # Generate a hash-based filename from the file path
    filename = os.path.basename(file_path)
    hash_value = md5(filename.encode()).hexdigest()
    _, extension = os.path.splitext(filename)
    new_filename = hash_value + extension
    return new_filename


@login_manager.user_loader
def load_user(username):
    # Query and return user from the database
    command = session.query(Command).filter_by(username=username).first()
    return command  # Возвращаем объект пользователя (Command) или None, если пользователь не найден

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
        if password1!=password2: return "Ведёные пароли не совпадают"

        # Сохраняем изображение в папку для загрузок
        # ДОБАВИТЬ ИЗМЕНЕНИЕ ИМЕНИ НА ХЕШ СУММУ
        # if team_photo.filename.endswith(('png', 'jpg', 'jpeg')):
        #     filename = team_photo.filename
        #     new_filename = rename_file_to_hash(filename)
        #     team_photo.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        
        if 'team_photo' not in request.files:
            return "Файл не был загружен"

        file = request.files['team_photo']
        if file.filename == '':
            return "Файл не выбран"
        
        if file:
            filename = secure_filename(file.filename)
            new_filename = rename_file_to_hash(filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], new_filename)
            file.save(file_path)
            # Теперь file_path содержит путь к загруженному файлу с хеш-именем
        


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
        login_user(command)
        return redirect(url_for('team'))
            
    return render_template('login.html')

@app.route('/dashboard')
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


# Личный каббинет команды
# Страница личного кабинета команды
# @app.route('/team', methods=['GET', 'POST'])
# def team():
#     if not current_user.is_authenticated: return redirect(url_for('login'))
#     command = session.query(Command).filter_by(username=current_user.username).first()

#     if request.method == 'POST':
#         command.team_name = request.form['team_name']
#         command.team_info = request.form['team_info']
#         command.image = request.form['image']
#         command.username = request.form['username']
#         command.password = request.form['password']
#         try:
#             session.add_all([command])
#             session.commit()
#             return redirect(url_for('login'))
#         except Exception as ex:
#             print(ex)
#             return "Проиошла оибка"
#     return render_template('lk.html', command=command)

@app.route('/team', methods=['GET', 'POST'])
def team():
    if not current_user.is_authenticated: return redirect(url_for('login'))
    command = session.query(Command).filter_by(username=current_user.username).first()
    users = command.users
    if request.method == 'POST':
        
        command.team_name = request.form['team_name']
        command.team_info = request.form['team_info']
        command.username = request.form['username']
        command.password = request.form['password']

        # Обработка загрузки изображения команды
        if 'team_image' in request.files:
            file = request.files['team_image']
            if file.filename != '':
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                file = rename_file_to_hash(f"static/uploads/{file.filename}")
                command.image = os.path.join('uploads', file)


        session.commit()

        
    if current_user.is_authenticated: return render_template('lk.html', command=command, users=users)
    return redirect(url_for('login'))

# Добавление нового участника
@app.route('/add_user', methods=['POST'])
def add_user():
    FIO = request.form['FIO']
    user_info = request.form['user_info']


    # Обработка загрузки изображения пользователя
    new_user = User(FIO=FIO, user_info=user_info)

    if 'user_image' in request.files:
        file = request.files['user_image']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file = rename_file_to_hash(f"static/uploads/{file.filename}")
            new_user.user_image = os.path.join('uploads', file)
    command = session.query(Command).filter_by(username=current_user.username).first()
    new_user.commands.append(command)
    
    
    session.add(new_user)
    session.commit()

    return redirect(url_for('team'))

@app.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['user_id']
    FIO = request.form['FIO']
    user_info = request.form['user_info']

    user = session.query(User).get(user_id)
    if user:
        user.FIO = FIO
        user.user_info = user_info
        session.commit()

    return redirect(url_for('team'))


if __name__ == '__main__':
    app.run(debug=True)



