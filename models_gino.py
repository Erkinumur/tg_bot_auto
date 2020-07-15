import asyncio
from gino import Gino
from sqlalchemy import (Column, Integer, BigInteger, String,
                        Sequence, ForeignKey, Float, Text, DateTime, sql)
from sqlalchemy.orm import relationship


from config import db_pass, db_user, host

db = Gino()


class User(db.Model):
    __tablename__ = 'tg_users'

    tg_id = Column(BigInteger, primary_key=True)
    full_name = Column(String(100))
    username = Column(String(50))


class Brand(db.Model):
    __tablename__ = 'brands'

    id = Column(Integer, Sequence('brand_id_seq'), primary_key=True)
    name = Column(String(50))

    models= relationship('CarModel', back_populates='brand', cascade='all, delete, delete-orphan')
    # query: sql.Select

    def __str__(self):
        return self.name


class CarModel(db.Model):
    __tablename__ = 'models'

    id = Column(Integer, Sequence('model_id_seq'), primary_key=True)
    name = Column(String(100))
    brand_id = Column(Integer, ForeignKey('brands.id'))

    brand = relationship('Brand', back_populates='brands')
    cars = relationship('Car', back_populates='model')
    query: sql.Select


class Car(db.Model):
    __tablename__ = 'cars'

    id = Column(Integer, Sequence('car_id_seq'), primary_key=True)
    title = Column(String(200))
    year = Column(Integer)
    kilometerage = Column(BigInteger)
    color = Column(String(50))
    volume = Column(Float)
    fuel_type = Column(String(50))
    engine_power = Column(Integer)
    wheel_drive = Column(String(30))
    gear_box = Column(String(30))
    wheel_position = Column(String(30))
    description = Column(Text)
    created_at = Column(DateTime)
    model_id = Column(Integer, ForeignKey('models.id'))
    owner = Column(BigInteger, ForeignKey('users.tg_id'))

    model = relationship('CarModel', back_populates='cars')
    user = relationship('User', back_populates='cars')
    query: sql.Select


async def create_db():
    await db.set_bind(f'postgresql://erkin:1535759460t@localhost/ginotest')

    # Create tables
    # db.gino: GinoSchemaVisitor
    # await db.gino.drop_all()
    await db.gino.create_all()


class DBCommands():

    async def get_all_brands(self):
        brands = await Brand.query.gino.all()
        return brands

    async def get_brand(self):
        brand = await Brand.get(1)
        return brand
