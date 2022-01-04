from aiogram import Dispatcher
from gino import Gino
from gino.schema import GinoSchemaVisitor

from data import config

db = Gino()


async def on_startup(disptacher: Dispatcher):
    print('Устаналиваем связь с Postgresql')


async def create_db():
    await db.set_bind(config.POSTGRES_URI)
    db.gino: GinoSchemaVisitor
    await db.gino.create_all()