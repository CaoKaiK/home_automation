from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from app import db

class Room(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    things = db.relationship('Thing', backref='location', lazy='dynamic') # pylint: disable=maybe-no-member

    def __repr__(self):
        return f'<Room {self.name}>'

class Thing(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    # category_id
    created_on = Column(DateTime, default=datetime.utcnow)
    room_id = Column(Integer, ForeignKey('room.id'))

    def __repr__(self):
        return f'<Thing {self.name}>'
