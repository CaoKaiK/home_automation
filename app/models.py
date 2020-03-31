from datetime import datetime
from app import db

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True)
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    things = db.relationship('Thing', backref='location', lazy='dynamic')

    def __repr__(self):
        return f'<Room {self.name}>'

class Thing(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), index=True, unique=True)
    # category_id
    created_on = db.Column(db.DateTime, default=datetime.utcnow)
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'))

    def __repr__(self):
        return f'<Thing {self.name}>'
