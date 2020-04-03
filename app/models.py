from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from marshmallow import Schema, fields
from app import db, ma

class Room(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    things = db.relationship('Thing', backref='location', lazy='dynamic') # pylint: disable=maybe-no-member

    @property
    def total_things(self):
        return len(self.things.all())

    def insert(self):
        db.session.add(self)
        db.session.commit()
    
    def patch(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return f'<Room {self.name}>'
    


class Thing(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(24), index=True, unique=True)
    created_on = Column(DateTime, default=datetime.utcnow)
    room_id = Column(Integer, db.ForeignKey('room.id')) # pylint: disable=maybe-no-member
    status = Column(Boolean, default=False)
    last_switched = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Thing {self.name}>'


class RoomSchema(Schema):    
    id = fields.Int()
    name = fields.String()
    created_on = fields.DateTime()
    total_things = fields.Int()
    things = fields.Nested('ThingSchema', many=True, only=['id', 'name'])
    

class ThingSchema(Schema):
    id = fields.Int()
    name = fields.String()
    created_on = fields.DateTime()
    location = fields.Nested(RoomSchema, only=['id', 'name'])
    status = fields.Boolean()
    last_switched = fields.DateTime()
