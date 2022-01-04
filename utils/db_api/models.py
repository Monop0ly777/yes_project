from sqlalchemy import Column, BigInteger, String, Integer, sql, Sequence
from utils.db_api.db_gino import db
import datetime
from typing import List
import sqlalchemy as sa
import pytz


#
# class BaseModel(db.Model):
#     __abstract__ = True
#
#     def __str__(self):
#         model = self.__class__.__name__
#         table: sa.Table = sa.inspect(self.__class__)
#         primary_key_columns: List[sa.Column] = table.primary_key.columns
#         values = {
#             column.name: getattr(self, self._column_name_map[column.name])
#             for column in primary_key_columns
#         }
#         values_str = " ".join(f"{name}={value!r}" for name, value in values.items())
#         return f"<{model} {values_str}>"


class TimedBaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(
        db.DateTime(True),
        default=db.func.now(tz=pytz.timezone('Europe/Kiev')),
        onupdate=db.func.now(tz=pytz.timezone('Europe/Kiev')),
        server_default=db.func.now(tz=pytz.timezone('Europe/Kiev')),

    )
    updated_at = db.Column(
        db.DateTime(True),
        default=db.func.now(tz=pytz.timezone('Europe/Kiev')),
        onupdate=db.func.now(tz=pytz.timezone('Europe/Kiev')),
        server_default=db.func.now(tz=pytz.timezone('Europe/Kiev')),
    )


class User(TimedBaseModel):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    user_id = Column(BigInteger)
    name = Column(String)
    yes_coin_balance = Column(Integer, default=0)

    query: sql.Select


class Item(TimedBaseModel):
    __tablename__ = 'items'
    id = Column(BigInteger, primary_key=True)
    category_code = Column(db.String(20))
    category_name = Column(db.String(50))

    subcategory_code = Column(db.String(20))
    subcategory_name = Column(db.String(50))
    promocode_index = Column(db.String(50), nullable=True)
    name = Column(db.String(50))
    text = Column(db.String(250))
    price = Column(Integer)

    query: sql.Select

    def __repr__(self):
        return f"""
Назва - {self.name}
Ціна - {self.price} YesCoins

Інформація - {self.text}
"""


class Staff(TimedBaseModel):
    __tablename__ = 'staff'
    id = Column(BigInteger, primary_key=True)
    name = Column(db.String(100))
    user_id = Column(BigInteger)
    position = Column(db.String(50))

    def __repr__(self):
        return f"{self.user_id}"


class Purchase(TimedBaseModel):
    __tablename__ = 'purchase'
    id = Column(BigInteger, primary_key=True)
    name = Column(db.String(100))
    status = Column(db.String(50))
    quantity = Column(Integer)
    sum = Column(Integer)
    number = Column(db.String(20))
    login = Column(db.String(100))
    user_id = Column(BigInteger, unique=False)

    def __repr__(self):
        return f"{self.name} - {self.sum}"


class Purchase_Confirmed(TimedBaseModel):
    __tablename__ = 'purchase_confirmed'
    id = Column(BigInteger, primary_key=True)
    name = Column(db.String(100))
    quantity = Column(Integer)
    status = Column(db.String(50))
    sum = Column(Integer)
    number = Column(db.String(20))
    login = Column(db.String(100))
    user_id = Column(BigInteger, unique=False)

    def __repr__(self):
        return f"{self.name} - {self.sum}"


class Promocodes(TimedBaseModel):
    __tablename__ = "promocodes"
    id = Column(BigInteger, primary_key=True)
    index = Column(db.String(100))
    data = Column(db.String(200), default=0)

class Promocodes_orders(TimedBaseModel):
    __tablename__ = "promocodes_orders"
    id = Column(BigInteger, primary_key=True)
    data = Column(db.String(200), default=0)
    name = Column(db.String(100))
    quantity = Column(Integer)
    sum = Column(Integer)
    login = Column(db.String(100))
    user_id = Column(BigInteger, unique=False)