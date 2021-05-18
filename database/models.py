import datetime
import enum
from sqlalchemy import *
from flask_login import UserMixin
from database.db_session import SqlAlchemyBase


class User(UserMixin, SqlAlchemyBase):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    login = Column(String(16), index=True, unique=True)
    email = Column(String, index=True, unique=True)
    password = Column(String, nullable=False)
    admin = Column(Boolean, nullable=False, default=False)
    created_date = Column(DateTime(timezone=True), default=datetime.datetime.now, nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.artist_id'), nullable=True, unique=True)

    def get_id(self):
        return self.user_id

    def to_dict(self):
        return {
            "id": self.user_id,
            "login": self.login,
        }


class Artist(SqlAlchemyBase):
    __tablename__ = 'artist'

    artist_id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.artist_id,
            "name": self.name,
        }


class Track(SqlAlchemyBase):
    __tablename__ = 'music'

    track_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.artist_id'), index=True, nullable=False)

    def to_dict(self):
        return {
            "id": self.track_id,
            "name": self.name,
            "artist_id": self.artist_id
        }
