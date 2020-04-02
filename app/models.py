from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from marshmallow import Schema, fields
from app import db, ma

class Room(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    things = db.relationship('Thing', backref='location', lazy='dynamic') # pylint: disable=maybe-no-member

    @property
    def things_in_room(self):
        return len(self.things.all())


    def __repr__(self):
        return f'<Room {self.name}>'


    

class Thing(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    # category_id
    created_on = Column(DateTime, default=datetime.utcnow)
    room_id = Column(Integer, db.ForeignKey('room.id')) # pylint: disable=maybe-no-member

    def __repr__(self):
        return f'<Thing {self.name}>'


class RoomSchema(Schema):    
    id = fields.Int()
    name = fields.String()
    created_on = fields.DateTime()
    things = fields.Nested('ThingSchema', many=True, only=['id', 'name'])
    

class ThingSchema(Schema):
    id = fields.Int()
    name = fields.String()
    created_on = fields.DateTime()
    location = fields.Nested(RoomSchema, only=['id', 'name'])
