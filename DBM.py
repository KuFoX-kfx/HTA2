from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from CDMM import Command, User, connect

# Устанавливаем соединение с базой данных
engine = create_engine('sqlite:///example.db')
Session = sessionmaker(bind=engine)
session = Session()
# Создаем таблицы, если они еще не созданы
connect('sqlite:///example.db')

# Создаие команды
# command1 = Command(name='Team A', image='123123png', email='dasdasd', username='wqeqweq', password='asd131')
# Добавляем команды в базу данных
# session.add_all([command1])
# session.commit()

# Создание пользоватея
#user1 = User(FIO='FSF DFSf sDFS', user_image='asdadapng', user_info="sadasdasdqwrscaf")
# Связывание человека и команды
#user1.commands.append(command1)
# Добавляем пользователей в базу данных
# session.add_all([user1])
# session.commit()

# Запрос данных: получаем все команды пользователя John Doe
johns_commands = session.query(User).filter_by(FIO='FSF DFSf sDFS').first().commands
print(f"Commands of John Doe: {[cmd.name for cmd in johns_commands]}")

# Запрос данных: получаем всех пользователей команды Team A
team_a_users = session.query(Command).filter_by(name='Team A').first().users
print(f"Users in Team A: {[user.FIO for user in team_a_users]}")


# Закрываем сессию
session.close()
