from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    orders = db.relationship('Order', backref='user', lazy=True)

order_table = db.Table('order_product', 
    db.Column('order_id', db.Integer, db.ForeignKey('order.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('product.id'), primary_key=True)
)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    #many to many reletionship with product class
    products = db.relationship('Product', secondary=order_table, lazy=True, backref=db.backref('order', lazy=True))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))


def insert_data():
    from datetime import datetime

    #create user
    user1 = User(name='Python User', date_joined=datetime.now())
    user2 = User(name='Flask User', date_joined=datetime.now())
    user3 = User(name='My User', date_joined=datetime.now())
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)

    #adding orders to user
    order1 = Order(total=99, user=user1)
    order2 = Order(total=293, user=user2)
    order3 = Order(total=29, user=user3)
    db.session.add(order1)
    db.session.add(order2)
    db.session.add(order3)

    #commit to the database
    db.session.commit()

def update_user():
    first_user = User.query.filter_by(id=1).first()
    first_user.name = 'Flask User'
    db.session.commit()

def delete_user():
    user = User.query.filter_by(id=1).first()
    db.session.delete(user)
    db.session.commit()

def query_table():
    first_user = User.query.filter_by(id=1).first()
    second_user = User.query.filter_by(id=2).first()
    third_user = User.query.filter_by(id=3).first()

    print('First User')
    for order in first_user.orders:
        print(f'Order ID: { order.id} Total: {order.total}')

    print('Second User')
    for order in second_user.orders:
        print(f'Order ID: { order.id} Total: {order.total}')

    print('Third User')
    for order in third_user.orders:
        print(f'Order ID: { order.id} Total: {order.total}')

def add_products():
    product1 = Product(name='Product One')
    product2 = Product(name='Product Two')
    product3 = Product(name='Product Three')

    db.session.add_all([product1, product2, product3])

    order_1 = Order.query.filter_by(id=1).first()
    order_1.products.append(product1)
    order_1.products.append(product2)

    order2 = Order.query.filter_by(id=2).first()
    order2.products.append(product3)

    db.session.commit()

def query_order_products():
    order1 = Order.query.filter_by(id=1).first()
    order2 = Order.query.filter_by(id=2).first()

    print('First Order Products')
    for product in order1.products:
        print(f'Product Name: {product.name} ')

    print('Second Order Products')
    for product in order2.products:
        print(f' Product Name: {product.name} ')

def get_all_users():
    users = User.query.all()
    for user in users:
        print(f' User Name: {user.name} ')

    user_count = User.query.count()
    print(f'User count: {user_count} ')
