from data_base.create_database import Favourite, BotUsers, Top3Photo, Blacklist
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from data_base.settings import USER, PASSWORD, HOST, DB_NAME

# Создание подключения к базе данных
connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
engine = create_engine(connection_string)
Base = declarative_base()

Session = sessionmaker(bind=engine)


def add_bot_users(vk_id, city, age, gender):
    try:
        session = Session()
        user = BotUsers(vk_id=vk_id, city=city, age=age, gender=gender)
        session.add(user)
        session.commit()
    except Exception:
        session = Session()
        session.rollback()


def add_favorite(botusers_id, vk_id, link, name, surname):
    try:
        session = Session()
        favorite = Favourite(botusers_id=botusers_id, vk_id=vk_id, name=name, link=link, surname=surname)
        session.add(favorite)
        session.commit()
    except Exception:
        session = Session()
        session.rollback()


def add_top3(favourites_id, photos):
    try:
        if len(photos) == 1:
            photo_1 = photos[0]
            photo_2 = None
            photo_3 = None
        elif len(photos) == 2:
            photo_1 = photos[0]
            photo_2 = photos[1]
            photo_3 = None
        elif len(photos) == 3:
            photo_1 = photos[0]
            photo_2 = photos[1]
            photo_3 = photos[2]
        else:
            photo_1 = None
            photo_2 = None
            photo_3 = None
        session = Session()
        top3 = Top3Photo(favourites_id=favourites_id, photo_1=photo_1, photo_2=photo_2, photo_3=photo_3)
        session.add(top3)
        session.commit()
    except Exception:
        session = Session()
        session.rollback()


def add_blacklist(botusers_id, vk_id):
    try:
        session = Session()
        blacklist = Blacklist(botusers_id=botusers_id, vk_id=vk_id)
        session.add(blacklist)
        session.commit()
    except Exception:
        session = Session()
        session.rollback()
