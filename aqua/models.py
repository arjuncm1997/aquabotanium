from aqua import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


class Login(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80),default='NULL')
    address = db.Column(db.String(80),default='NULL')
    status=db.Column(db.String(80),default='NULL')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    usertype = db.Column(db.String(80), nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)


class Products(db.Model):  
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    brand = db.Column(db.String(80))
    price = db.Column(db.String(80))
    image = db.Column(db.String(20), default='default.jpg')