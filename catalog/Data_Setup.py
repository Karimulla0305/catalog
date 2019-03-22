import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class TabletCompanyName(Base):
    __tablename__ = 'tabletcompanyname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="tabletcompanyname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class TabletName(Base):
    __tablename__ = 'tabletname'
    id = Column(Integer, primary_key=True)
    name = Column(String(350), nullable=False)
    price = Column(String(10))
    discription = Column(String(350), nullable=False)
    power = Column(String(10))
    tabletcompanynameid = Column(Integer, ForeignKey('tabletcompanyname.id'))
    tabletcompanyname = relationship(
        TabletCompanyName, backref=backref('tabletname',
                                           cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="tabletname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self. name,
            'price': self. price,
            'discription': self.discription,
            'power': self.power,
            'id': self. id
        }

engin = create_engine('sqlite:///tablets.db')
Base.metadata.create_all(engin)
