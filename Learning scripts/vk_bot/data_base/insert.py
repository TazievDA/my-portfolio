
from data_base.models import Favourite, BotUsers, Top3Photo, Blacklist
from data_base.settings import USER, PASSWORD, HOST, DB_NAME

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError


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
    top_photos = {}
    for number, photo in enumerate(photos[:3]):
        top_photos[f"photo_{number + 1}"] = photo

    session = Session()
    try:
        top3 = Top3Photo(favourites_id=favourites_id, **top_photos)
        session.add(top3)
        session.commit()
    except SQLAlchemyError as error:
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
