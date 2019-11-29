import sqlalchemy as sa
import json 
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()

class Album(Base):
    """
    Описывает структуру таблицы album для хранения 
    записей музыкальной библиотеки
    """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает 
    таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

def find_art(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums 

def find_alb(new_album):
    """
    Находит альбом в базе данных по введенному пользователем
    новому альбому для проверки повторений и выдает ошибку HTTP 409.
    """
    session = connect_db()
    album_new = session.query(Album).filter(Album.album == new_album).all()
    return album_new

def write_new_album(data_new):
    """Записывает данные в базу и проверяет на наличие альбома 
        в базе через функцию = "find_alb" """
    cash_record = data_new
    #print('{} \n {} \n {} \n {} \n'.format(cash_record['year'], cash_record['artist'], cash_record['genre'], cash_record['album']))
    year = cash_record['year']
    artist = cash_record['artist']
    genre = cash_record['genre']
    album = cash_record['album']

    newalbum = Album(
        year=year,
        artist = artist,
        genre = genre,
        album = album,
        )
    print('Данные оформлены для занесения в БД: \n {} \n {} \n {} \n {} \n'.format(newalbum.year, newalbum.artist, newalbum.genre, newalbum.album))
    session = connect_db()
    session.add(newalbum)
    session.commit()

    album_new = find_alb(cash_record['album'])
    album_names = [album.album for album in album_new]
    result = '{}'.format(album_names)
    print( 'Альбом {} : записан в БАЗУ ДАННЫХ'.format(result))
    return 'Доехали!'

