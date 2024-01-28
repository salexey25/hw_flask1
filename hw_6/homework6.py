"""
Необходимо создать базу данных для интернет-магазина. База данных должна состоять из трёх таблиц: товары, заказы и пользователи.
— Таблица «Товары» должна содержать информацию о доступных товарах, их описаниях и ценах.
— Таблица «Заказы» должна содержать информацию о заказах, сделанных пользователями.
— Таблица «Пользователи» должна содержать информацию о зарегистрированных пользователях магазина.
• Таблица пользователей должна содержать следующие поля: id (PRIMARY KEY), имя, фамилия, адрес электронной почты и пароль.
• Таблица заказов должна содержать следующие поля: id (PRIMARY KEY), id пользователя (FOREIGN KEY), id товара (FOREIGN KEY), дата заказа и статус заказа.
• Таблица товаров должна содержать следующие поля: id (PRIMARY KEY), название, описание и цена.

Создайте модели pydantic для получения новых данных и возврата существующих в БД для каждой из трёх таблиц (итого шесть моделей).
Реализуйте CRUD операции для каждой из таблиц через создание маршрутов, REST API (итого 15 маршрутов).
* Чтение всех
* Чтение одного
* Запись
* Изменение
* Удаление
"""

from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

DATABASE_URL = "sqlite:///hw9_database.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
templates = Jinja2Templates(directory='templates')

"""Определяем модели таблиц User, Product, Order"""
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(50))
    password = Column(String(5))
    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(50))
    price = Column(Integer)
    orders = relationship("Order", back_populates="product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String(50))
    user = relationship("User", back_populates="orders")
    product = relationship("Product", back_populates="orders")

"""Создаем классы для валидации входных данных"""
class UserCreate(BaseModel):
    first_name: str = Field(title="First_name", max_length=50)
    last_name: str = Field(title="Last_name", max_length=50)
    email: str = Field(title="Email", max_length=50)
    password: str = Field(title="Password", max_length=50)

class ProductCreate(BaseModel):
    name: str = Field(title="Name", max_length=50)
    description: str = Field(title="Description", max_length=50)
    price: str = Field(title="Price", max_length=50)

class OrderCreate(BaseModel):
    user_id: int
    product_id: int
    status: str


Base.metadata.create_all(bind=engine)

"""Создаем маршруты"""

"""CRUD для таблицы User"""

@app.post("/users/")
async def create_user(user: UserCreate):
    db = SessionLocal()
    db_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/")
async def read_users():
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return users

@app.get("/users/{user_id}")
async def read_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()
    return user

@app.put("/users/{user_id}")
async def update_user(user_id: int, first_name: str = None, last_name: str = None, email: str = None, password: str = None):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        if first_name:
            user.first_name = first_name
        if last_name:
            user.last_name = last_name
        if email:
            user.email = email
        if password:
            user.password = password
        db.commit()
        db.refresh(user)
    db.close()
    return user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()
    return user

"""CRUD для таблицы Product"""

@app.post("/product/")
async def create_product(product: ProductCreate):
    db = SessionLocal()
    db_product = Product(name=product.name, description=product.description, price=product.price)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.get("/product/")
async def read_products():
    db = SessionLocal()
    products = db.query(Product).all()
    db.close()
    return products

@app.get("/products/{product_id}")
async def read_products(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    db.close()
    return product

@app.put("/products/{product_id}")
async def update_product(product_id: int, name: str = None, description: str = None, price: str = None):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        if name:
            product.name = name
        if description:
            product.description = description
        if price:
            product.price = price
        db.commit()
        db.refresh(product)
    db.close()
    return product

@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if product:
        db.delete(product)
        db.commit()
    db.close()
    return product


"""CRUD для таблицы Order"""

@app.post("/orders/")
async def create_order(order: OrderCreate):
    db = SessionLocal()
    db_order = Order(user_id=order.user_id, product_id=order.product_id, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

@app.get("/orders/")
async def read_orders():
    db = SessionLocal()
    orders = db.query(Order).all()
    db.close()
    return orders

@app.get("/orders/{order_id}")
async def read_orders(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    db.close()
    return order

@app.put("/orders/{order_id}")
async def update_order(order_id: int, user_id: int = None, product_id: int = None, status: str = None):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        if user_id:
            order.user_id = user_id
        if product_id:
            order.product_id = product_id
        if status:
            order.status = status
        db.commit()
        db.refresh(order)
    db.close()
    return order

@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    db = SessionLocal()
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    db.close()
    return order
