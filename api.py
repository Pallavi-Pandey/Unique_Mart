from flask import request
from flask_restful import Resource,marshal_with, fields,reqparse,abort
from models import *
from datetime import datetime

# def abort_if_todo_doesnt_exist(todo_id,T):
#     if todo_id not in TODOS:
#         abort(404, message="Todo {} doesn't exist".format(todo_id))

prod_parser = reqparse.RequestParser()
prod_parser.add_argument('product_name')
prod_parser.add_argument('price')
prod_parser.add_argument('manufacture_date')
prod_parser.add_argument('expiry_date')
prod_parser.add_argument('quantity')
prod_parser.add_argument('category_id')

class Product_api(Resource):
    output = {"id": fields.String,
              "product_name":fields.String,
              "price":fields.String,
              "manufacture_date":fields.String,
              "expiry_date":fields.String,
              "quantity":fields.String,
              "category_id":fields.String,
              }

    @marshal_with(output)
    def get(self,product_id):
        prod = Product.query.filter_by(id=product_id).first()
        if not prod:
            abort(404, message="Product not found")
        return prod
    
    @marshal_with(output)
    def post(self):
        data = prod_parser.parse_args()
        print(data.get('product_name'))
        product = Product(product_name=data.get('product_name'), price=data.get('price'), 
                       manufacture_date=datetime.strptime(data.get('manufacture_date'), '%Y-%m-%d').date(), 
                       expiry_date=datetime.strptime(data.get('expiry_date'), '%Y-%m-%d').date(),
                       quantity=data.get('quantity'),category_id=data.get('category_id'),image_link=data.get('image_link'))

        print("jbk")
        db.session.add(product)
        db.session.commit()
        db.session.refresh(product)
        return product
    
    def delete(self,product_id):
        prod = Product.query.filter_by(id=product_id).first()
        db.session.delete(prod)
        db.session.commit()
        return prod.product_name+" deleted successfuly"  
    
    @marshal_with(output)
    def put(self,product_id):
        data = prod_parser.parse_args()
        pro = Product.query.filter_by(id=product_id).first()
        pro.product_name=data.get('product_name')
        pro.price=data.get('price')
        pro.manufacture_date=datetime.strptime(data.get('manufacture_date'), '%Y-%m-%d').date()
        pro.expiry_date=datetime.strptime(data.get('expiry_date'), '%Y-%m-%d').date()
        pro.quantity=data.get('quantity')
        pro.image_link=data.get('image_link')
        db.session.add(pro)
        db.session.commit()
        db.session.refresh(pro)
        return pro

cat_parser = reqparse.RequestParser()
cat_parser.add_argument('name')

class Category_api(Resource):
    output = {"id": fields.String,
              "name":fields.String}
    
    @marshal_with(output)
    def get(self,category_id):
        cat = Category.query.filter_by(id=category_id).first()
        if not cat:
            abort(404, message="Category not found")
        return cat
    
    @marshal_with(output)
    def post(self):
        data = cat_parser.parse_args()
        print(data)
        print(data.get('name'))
        category = Category(name=data.get('name'))
        db.session.add(category)
        db.session.commit()
        db.session.refresh(category)
        return category
    
    def delete(self,category_id):
        cat = Category.query.filter_by(id=category_id).first()
        db.session.delete(cat)
        db.session.commit()
        return cat.name+" deleted successfuly"
    
    @marshal_with(output)
    def put(self,category_id):
        data = cat_parser.parse_args()
        cat = Category.query.filter_by(id=category_id).first()
        cat.name=data.get('name')
        db.session.add(cat)
        db.session.commit()
        db.session.refresh(cat)
        return cat

class CategoryList(Resource):
    @marshal_with({"categories": fields.List(fields.Nested(Category_api.output))})
    def get(self):
        cats = Category.query.all()
        return {"categories": cats}

class ProductList(Resource):
    @marshal_with({"products": fields.List(fields.Nested(Product_api.output))})
    def get(self):
        prods = Product.query.all()
        return {"products": prods}
