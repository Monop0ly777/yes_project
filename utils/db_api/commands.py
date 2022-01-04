from typing import List

from asyncpg import UniqueViolationError
from sqlalchemy import and_

from utils.db_api.db_gino import db
from utils.db_api.models import User, Item, Staff, Purchase, Purchase_Confirmed, Promocodes, Promocodes_orders


async def add_item(**kwargs):
    new_item = await Item(**kwargs).create()
    return new_item


async def add_user(user_id: int, name: str):
    try:
        user = User(user_id=user_id, name=name)
        await user.create()
    except UniqueViolationError:
        pass


async def select_all_users():
    users = await User.query.gino.all()
    return users


async def select_user(user_id: int):
    user = await User.query.where(User.user_id == user_id).gino.first()
    return user


async def count_users():
    total = await db.func.count(User.user_id).gino.scalar()
    return total


async def get_categories() -> List[Item]:
    return await Item.query.distinct(Item.category_code).gino.all()


async def get_subcategories(category) -> List[Item]:
    return await Item.query.distinct(Item.subcategory_code).where(Item.category_code == category).gino.all()


async def get_items(category_code, subcategory_code) -> List[Item]:
    items = await Item.query.where(
        and_(Item.category_code == category_code, Item.subcategory_code == subcategory_code)
    ).gino.all()
    return items


async def get_item(item_id) -> Item:
    item = await Item.query.where(Item.id == item_id).gino.first()
    return item


async def spend_balance(user_id, amount):
    await User.update.values(yes_coin_balance=User.yes_coin_balance - amount).where(
        User.user_id == user_id).gino.status()


async def select_staff_admin():
    staff = await Staff.query.where(Staff.position == 'Админ').gino.all()
    return staff


async def select_staff_manager():
    staff = await Staff.query.where(Staff.position == 'Менеджер').gino.all()
    return staff


async def select_staff():
    staff = await Staff.query.gino.all()
    return staff


async def add_purchase(name, quantity, sum, number, login, user_id, status):
    purchase = Purchase(user_id=user_id, name=name, quantity=quantity, sum=sum, number=number, login=login,
                        status=status)
    await purchase.create()


async def add_purchase_promocodes(name, quantity, sum, login, user_id, data):
    purchase = await Promocodes_orders(user_id=user_id, name=name, quantity=quantity, sum=sum, login=login, data=data).create()


async def add_purchase_confirmed(name, quantity, sum, number, login, user_id):
    purchase_confirmed = Purchase_Confirmed(user_id=user_id, name=name, quantity=quantity, sum=sum, number=number,
                                            login=login)
    await purchase_confirmed.create()


async def get_purchases() -> List[Item]:
    return await Purchase.query.gino.all()


async def get_purchases_complete() -> List[Item]:
    return await Purchase_Confirmed.query.gino.all()


async def get_purchases_id(id: int):
    return await Purchase.query.where(Purchase.id == id).gino.first()


async def get_purchases_complete_id(id: int):
    return await Purchase_Confirmed.query.where(Purchase_Confirmed.id == id).gino.first()


async def get_purchases_change_status(id: int, status):
    await Purchase.update.values(status=status).where(Purchase.id == id).gino.status()


async def purchases_status_successful(id, name, quantity, status, sum, number, login, user_id):
    await Purchase.delete.where(Purchase.id == id).gino.all()
    await Purchase_Confirmed(name=name, quantity=quantity, status=status, sum=sum, number=number, login=login,
                             user_id=user_id).create()


async def delete_complete_order_command(id: int):
    await Purchase_Confirmed.delete.where(Purchase_Confirmed.id == id).gino.all()


async def get_promocode(index, quantity):
    x = await Promocodes.query.limit(quantity).where(Promocodes.index == index).gino.all()
    for i in x:
        await Promocodes.delete.where(and_(Promocodes.index == index, Promocodes.data == i.data)).gino.status()
    return x


async def get_promocodes_count(index):
    x = await Promocodes.query.where(Promocodes.index == index).gino.all()
    return x


async def promocodes_successful(index, data, name, quantity, sum, login, user_id):
    await Promocodes_orders(index=index, data=data, name=name, quantity=quantity, sum=sum, login=login,
                                user_id=user_id).create()
