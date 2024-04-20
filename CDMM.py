from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Создаем объект базы данных
Base = declarative_base()

# Промежуточная таблица для связи многие-ко-многим между командами и пользователями
association_table = Table('user_commands', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('command_id', Integer, ForeignKey('commands.id'))
)

# Модель данных для команд
class Command(Base):
    __tablename__ = 'commands'
    id = Column(Integer, primary_key=True, autoincrement=True)
    team_name = Column(String,unique=True)
    team_info = Column(String)  
    image = Column(String)   
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    password = Column(String)
    
    # Связь многие ко многим с пользователями через промежуточную таблицу
    users = relationship('User', secondary=association_table, back_populates='commands')

# Модель данных для пользователей
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    FIO = Column(String)
    user_image = Column(String)
    user_info = Column(String)
    
    # Связь многие ко многим с командами через промежуточную таблицу
    commands = relationship('Command', secondary=association_table, back_populates='users')

# Функция для установления соединения с базой данных
def connect(database_url):
    engine = create_engine(database_url)
    Base.metadata.create_all(engine)  # Создаем таблицы, если они еще не созданы
    Session = sessionmaker(bind=engine)
    return Session()

