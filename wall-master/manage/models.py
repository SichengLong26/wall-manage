from datetime import datetime
from enum import unique 
from manage import db


class User(db.Model):
    __tablename__='user'
    uid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),unique=True)
    phone = db.Column(db.Integer)
    password = db.Column(db.String(20))
    # messages = db.relationship('Message','userinfo') # 联系

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

class Message(db.Model):
    __tablename__='message'
    mid = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    content = db.Column(db.String(200))
    fontSize = db.Column(db.Integer)
    centerRelX = db.Column(db.Float)
    centerRelY = db.Column(db.Float)
    width = db.Column(db.Float)
    height = db.Column(db.Float)
    borderRadius = db.Column(db.Float)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    user_uid = db.Column(db.Integer, db.ForeignKey('user.uid')) # 定义外键

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
