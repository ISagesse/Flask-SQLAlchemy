from app import app
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    date_joined = db.Column(db.DateTime)

    orders = db.relationship('Order', backref='user', lazy=True)

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

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