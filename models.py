from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
from flask_login import UserMixin
from datetime import datetime

class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    def get_id(self):
        return str(self.id)

class Admin(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    def get_id(self):
        return str(self.id)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    products = db.relationship('Product', back_populates='category', cascade='all, delete-orphan')

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(200), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    manufacture_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    quantity = db.Column(db.Integer, default=1)
    image_link = db.Column(db.String(200))

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='products')

class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    bought = db.Column(db.Boolean, default=False)
    T_time = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)

    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')


