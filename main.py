from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DBM import Base, Users, Commands

# Create an SQLite database engine
engine = create_engine('sqlite:///example.db')

# Create all tables defined in Base (i.e., User and Command)
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create and add users to the database
# Создаем несколько команд

    # Создаем несколько пользователей
user1 = Users(FIO='FSF DFSf sDFS', user_image='asdadapng', user_info="sadasdasdqwrscaf")
user2 = Users(FIO='FSF DFSf sDFS', user_image='asdadapng', user_info="sadasdasdqwrscaf")
session.add_all([user1, user2])
session.commit()

# Create and add commands to the database
# Создаем несколько команд
command1 = Commands(name='Team A', image='123123png', email='dasdasd', username='wqeqweq', password='asd131')
command2 = Commands(name='Team B', image='123123png', email='dasdasd', username='wqeqweq', password='asd131')

session.add_all([command1, command2])
session.commit()

# Associate users with commands
user1.commands.append(command1)
user2.commands.append(command1)
user2.commands.append(command2)
session.commit()

# Query and print user's commands
for user in session.query(Users).all():
    print(f"{user.name}'s Commands:")
    for command in user.commands:
        print(f"  - {command.name}: {command.description}")

# Close the session
session.close()
