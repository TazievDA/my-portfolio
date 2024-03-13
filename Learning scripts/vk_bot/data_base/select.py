
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, select
from sqlalchemy.orm import declarative_base

from data_base.settings import USER, PASSWORD, HOST, DB_NAME
from data_base.models import Favourite, BotUsers, Blacklist, Top3Photo

# Создание подключения к базе данных
connection_string = f"postgresql://{USER}:{PASSWORD}@{HOST}/{DB_NAME}"
engine = create_engine(connection_string, pool_size=1000)
Base = declarative_base()


def select_current_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    bot_users = BotUsers
    metadata.reflect(bind=engine)
    stmt = select(bot_users).where(bot_users.vk_id.in_([user_id]))
    return session.scalar(stmt).id


def check_current_user(user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    bot_users = BotUsers
    metadata.reflect(bind=engine)
    stmt = (select(bot_users)
            .where(bot_users.vk_id.in_([user_id])))
    return session.scalars(stmt).one_or_none()


def select_all_favorites(curent_user_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    favorites = Favourite
    metadata.reflect(bind=engine)
    stmt = (select(favorites.link, favorites.name, favorites.surname, Top3Photo.photo_1, Top3Photo.photo_2,
                   Top3Photo.photo_3)
            .join(BotUsers)
            .join(Top3Photo)
            .where(BotUsers.vk_id.in_([curent_user_id])))
    results = session.execute(stmt)

    favorites = [[row.link, row.name, row.surname, row.photo_1, row.photo_2, row.photo_3] for row in results]

    return favorites


def select_one_favorite(current_user_id, favorite_vk_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    stmt = (select(Favourite)
            .join(BotUsers)
            .where(BotUsers.vk_id == current_user_id)
            .where(Favourite.vk_id == favorite_vk_id))
    return session.scalars(stmt).one_or_none()


def select_blacklist(current_user_id, vk_id):
    Session = sessionmaker(bind=engine)
    session = Session()
    metadata = MetaData()
    metadata.reflect(bind=engine)
    stmt = (select(Blacklist)
            .join(BotUsers)
            .where(BotUsers.vk_id.in_([current_user_id]))
            .where(Blacklist.vk_id.in_([vk_id])))
    result = session.scalars(stmt).one_or_none()
    return result
