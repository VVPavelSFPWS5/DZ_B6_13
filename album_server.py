import os
import json
import datetime

from bottle import route
from bottle import run
from bottle import HTTPError
from bottle import request

import album # Подключаем файл album.py лежащий в одной дерриктории.
from album import write_new_album

class CustomError(TypeError):
    """ Ошибка - не верно указан год"""

@route("/albums/<artist>")
def albums(artist):
    albums_list = album.find_art(artist) # вызываем функцию поиска из модуля(файла) album
    if not albums_list:
        message = "Альбомов {} не найдено".format(artist)
        result = HTTPError(404, message)
    else:
        album_names = [album.album for album in albums_list]
            # 1. Веб-сервер принимает GET-запросы по адресу /albums/<artist> 
            #и выводит на экран сообщение с количеством альбомов s
            #исполнителя artist и списком названий этих альбомов: 
            #Добавили в result = "Количество альбомов : {} и ... .format(len(album_names),...
        result = "Количество альбомов : {}.<BR> Список альбомов {}: ".format(len(album_names),artist)
        result += ", ".join(album_names)
    return result

@route("/albums", method="POST") # Вызов из консоли =  http -f POST localhost:8080/albums year=2019 artist=Babkina genre=folk album=Kalinka
def user():
    """ 
    Получает данные от пользователя по POST протоколу
    и сохраняет в переменную, проверяет корректность 
    данных введеных пользователем с выводом ошибок,
    1. Год = int() - поднимает CustomError("Не верно указан год!")
    2. Имя артиста = str()CustomError("Не верно указан год!")
    3. Жанр исполнителя = str()CustomError("Не верно указан год!")
    4. Наименование альбома = str()CustomError("Не верно указан год!")
    5. при наличии альбома в базе - выдает ошибку HTTP 409.
    """
    d = datetime.date.today() # Берем текущую дату для проверки введенной пользователем.
    result = "Начало обработки запроса"
    # Забираем из запроса данные в словарь.
    cash_record = {
        "year": int(request.forms.get("year")), #Приводим сразу в формат int() 
        "artist": request.forms.get("artist"),
        "genre": request.forms.get("genre"),
        "album": request.forms.get("album")
    }
    # Проверяем введенный год пользователем.
    if 1000 <= cash_record['year'] <= d.year:
        pass
    else:
        raise CustomError("Не верно указан год!")
    # Проверяем наличие альбома в базе.    
    album_new = album.find_alb(cash_record['album'])
    if not album_new:
        album.write_new_album(cash_record)
        result = "Данные успешно отправлены для записи в БАЗУ"
    else:
        album_names = [album.album for album in album_new]
        result = HTTPError(409,'{} альбом с таким именем уже внесен !!!'.format(len(album_names), album_names))
    
    return result
if __name__ == "__main__":
    run(host="localhost", port=8080, debug=True)












    
