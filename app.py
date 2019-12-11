
# Full CRUD API using SQLAlchemy , Marshmallow


from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os


#  Init app
app = Flask(__name__)

# @app.route('/',methods=['GET'])

# #  go to postman and get : http://localhost:5000
# def get():
#     return jsonify({'msg':'Hello World'})

#  Basedir
basedir = os.path.abspath(os.path.dirname(__file__))
#  Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#  Init db --> Initialize sqlalchemy
db = SQLAlchemy(app)

#  Initi marshmallow
ma = Marshmallow(app)

#  Class for resource
class Product(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100), unique=True)
    desc = db.Column(db.String(200))
    price = db.Column(db.Float)
    qty = db.Column(db.Integer)

    def __init__(self, name,desc,price,qty):
        self.name = name
        self.desc = desc
        self.price = price
        self.qty = qty



# Product Schema - fields that you want to be visible in the endpoint
class Product_Schema(ma.Schema):
    class Meta:
        fields = ('id','name','desc','price','qty')

# to create DB we need to go to python shell and run following (ctrl + C --> python)
# from app import db
#  db.create_all()

# Init Schema
ProductSchema = Product_Schema()
ProductsSchema = Product_Schema(many = True)


#  Create Product
@app.route('/product',methods=['POST'])
def create_product():
    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    new_product = Product( name, desc, price, qty)
    db.session.add(new_product)
    db.session.commit()

    return ProductSchema.jsonify(new_product)
    

#  Get all products
@app.route('/product',methods=['GET'])
def get_all_products():
    all = Product.query.all()
    res =  ProductsSchema.dump(all)
    return jsonify(res)

#  Get single product
@app.route('/product/<id>',methods=['GET'])
def get_one_product(id):
    one_product = Product.query.get(id)
    return ProductSchema.jsonify(one_product)

# Update product
@app.route('/product/<id>',methods=['PUT'])
def update_product(id):
    one_product = Product.query.get(id)

    name = request.json['name']
    desc = request.json['desc']
    price = request.json['price']
    qty = request.json['qty']

    one_product.name = name
    one_product.desc = desc
    one_product.price = price
    one_product.qty = qty


    db.session.commit()
    return ProductSchema.jsonify(one_product)

#  Delete Product

@app.route('/product/<id>',methods=['Delete'])
def delete_product(id):
    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return ProductSchema.jsonify(product)

#  Run Server
if __name__ == "__main__":
    app.run(debug=True)