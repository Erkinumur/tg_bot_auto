import asyncio
import datetime

import peewee
import logging

from aiogram import types, exceptions
from peewee import DoesNotExist
from peewee_async import Manager, PostgresqlDatabase

database = PostgresqlDatabase('peewee_test')


class MyManager(Manager):
    database = database


objects = MyManager()


class User(peewee.Model):
    tg_id = peewee.BigIntegerField(primary_key=True)
    full_name = peewee.CharField(max_length=100)
    username = peewee.CharField(max_length=50)

    class Meta:
        database = database
        table_name = 'users'


class CarBrand(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    name = peewee.CharField(max_length=50)

    class Meta:
        database = database
        table_name = 'car_brands'

    def __str__(self):
        return self.name


class CarModel(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    name = peewee.CharField(max_length=50)
    brand = peewee.ForeignKeyField(CarBrand, backref='models', on_delete='CASCADE', )

    class Meta:
        database = database
        table_name = 'car_models'


class Car(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    title = peewee.CharField(max_length=250)
    model = peewee.ForeignKeyField(CarModel, backref='cars', on_delete='CASCADE')
    year = peewee.IntegerField()
    kilometerage = peewee.BigIntegerField(verbose_name='Пробег')
    color = peewee.CharField(max_length=30)
    volume = peewee.DecimalField()
    fuel_type = peewee.CharField(max_length=30, verbose_name='Тип топлива')
    wheel_drive = peewee.CharField(max_length=20, verbose_name='Привод')
    gear_box = peewee.CharField(max_length=30, verbose_name='Коробка передач')
    wheel_position = peewee.CharField(max_length=10, verbose_name='Расположение руля')
    description = peewee.TextField()
    price = peewee.IntegerField()
    created_at = peewee.DateTimeField(default=datetime.datetime.now())
    owner = peewee.ForeignKeyField(User, backref='cars', on_delete='CASCADE')

    class Meta:
        database = database
        table_name = 'cars'


class Image(peewee.Model):
    id = peewee.AutoField(primary_key=True)
    tg_id = peewee.CharField()
    car = peewee.ForeignKeyField(Car, backref='images', on_delete='CASCADE')

    class Meta:
        database = database
        table_name = 'images'


class DBCommands:
    async def get_user(self, user_id):
        user = await objects.get(User, tg_id=user_id)
        return user

    async def add_new_user(self, user_id):
        user = types.User.get_current()
        new_user, created = await objects.get_or_create(
            User, tg_id=user_id, defaults={
                'full_name': f'{user.first_name}  {user.last_name}',
                'username': user.username
            })

    async def get_brand(self, brand_pk):
        brand = await objects.get(CarBrand, id=brand_pk)
        return brand

    async def get_all_brands(self):
        brands = await objects.execute(CarBrand.select())
        return brands

    async def get_model(self, model_pk):
        model = await objects.get(CarModel, id=model_pk)
        return model

    async def get_models(self, brand_pk):
        models = await objects.execute(CarBrand.get(CarBrand.id == brand_pk).models.order_by(CarModel.name))
        return models

    async def add_new_img(self, file_id, car: Car):
        await objects.create(Image,
                             tg_id=file_id,
                             car=car)

    async def add_new_car(self, data: dict):
        user = await self.get_user(data.get('user_id'))
        car = await objects.create(
            Car,
            title=f'{data["brand"].name} {data["model"].name} ' \
                  f'{data["year"]}г. {data["price"]}',
            model=data.get('model'),
            year=data.get('year'),
            kilometerage=data.get('kilometerage'),
            color=data.get('color'),
            volume=data.get('volume'),
            fuel_type=data.get('fuel_type'),
            wheel_drive=data.get('wheel_drive'),
            gear_box=data.get('gear_box'),
            wheel_position=data.get('wheel_position'),
            description=data.get('description'),
            price=data.get('price'),
            owner=user,
        )

        for file_id in data.get('images'):
            await self.add_new_img(file_id, car)


def create_db():
    database.connect()
    print('connect')
    database.create_tables((User, CarBrand, CarModel, Car, Image))
    database.close()
    print('close')
