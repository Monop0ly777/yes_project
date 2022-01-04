from utils.db_api.models import Purchase_Confirmed, Promocodes_orders, User, Purchase, Staff


async def get_all_orders():
    return await Purchase.query.gino.all()


async def get_all_orders_complete():
    return await Purchase_Confirmed.query.gino.all()


async def get_all_orders_promocodes():
    return await Promocodes_orders.query.gino.all()


async def user_balance_update(id: int, amount):
    await User.update.values(yes_coin_balance=amount).where(User.user_id == id).gino.status()


async def user_balance_add(amount):
    await User.update.values(yes_coin_balance=User.yes_coin_balance + amount).gino.status()


async def user_balance_add_invd(amount, id):
    await User.update.values(yes_coin_balance=User.yes_coin_balance + amount).where(User.user_id == id).gino.status()


async def staff_add_db(user_id, position, name):
    staff = Staff(user_id=user_id, position=position, name=name)
    await staff.create()
