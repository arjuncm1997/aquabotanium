from aqua import db,app,login_manager
from flask_login import UserMixin
from flask_table import Table, Col, LinkCol
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(id):
    return Login.query.get(int(id))


class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.VARCHAR)
    email= db.Column(db.VARCHAR)
    phone= db.Column(db.Integer)
    subject = db.Column(db.VARCHAR)
    message= db.Column(db.VARCHAR)
    usertype= db.Column(db.VARCHAR)