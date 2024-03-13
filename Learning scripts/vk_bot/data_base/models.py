import sqlalchemy as sq
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import declarative_base, relationship

from data_base.settings import (USER, PASSWORD, HOST, DB_NAME)


# Создание подключения к базе данных
connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
engine = create_engine(connection_string)
Base = declarative_base()


# Создание классов для каждой таблицы
class BotUsers(Base):
    __tablename__ = 'bot_users'

    id = sq.Column(sq.Integer, primary_key=True)
    vk_id = sq.Column(sq.BigInteger)
    city = sq.Column(sq.Integer)
    age = sq.Column(sq.Integer)
    gender = sq.Column(sq.Integer)


class Favourite(Base):
    __tablename__ = 'favourites'

    id = sq.Column(sq.Integer, primary_key=True)
    botusers_id = sq.Column(sq.Integer, sq.ForeignKey("bot_users.id"))
    vk_id = sq.Column(sq.BigInteger)
    link = sq.Column(sq.String(200))
    name = sq.Column(sq.String(30))
    surname = sq.Column(sq.String(40))

    botusers = relationship(BotUsers, backref="favourites")


class Top3Photo(Base):
    __tablename__ = 'top3photo'

    id = sq.Column(sq.Integer, primary_key=True)
    favourites_id = sq.Column(sq.Integer, sq.ForeignKey('favourites.id'))
    photo_1 = sq.Column(sq.String)
    photo_2 = sq.Column(sq.String)
    photo_3 = sq.Column(sq.String)

    favourites = relationship(Favourite, backref="top3photo")


class Blacklist(Base):
    __tablename__ = 'blacklist'

    id = sq.Column(sq.Integer, primary_key=True)
    botusers_id = sq.Column(sq.Integer, sq.ForeignKey('bot_users.id'))
    vk_id = sq.Column(sq.BigInteger)

    botusers = relationship(BotUsers, backref="blacklist")

# Создание таблиц в базе данных
def create_tables(engine):
    #Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables(engine)
