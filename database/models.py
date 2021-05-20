import datetime
import enum
from sqlalchemy import *
from flask_login import UserMixin
from database.db_session import SqlAlchemyBase, create_session


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

    @staticmethod
    def get_by_id(id_):
        return create_session().query(Artist).filter(Artist.artist_id == id_).first()

    def to_dict(self):
        return {
            "id": self.artist_id,
            "name": self.name,
        }


class Track(SqlAlchemyBase):
    __tablename__ = 'music'

    track_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    uploaded_id = Column(Integer, ForeignKey('user.user_id'), index=True, nullable=False)
    artist_id = Column(Integer, ForeignKey('artist.artist_id'), index=True, nullable=False)

    @staticmethod
    def get_by_id(id_):
        return create_session().query(Track).filter(Track.user_id == id_).first()

    def to_dict(self):
        return {
            "id": self.track_id,
            "name": self.name,
            "artist_id": self.artist_id,
            "artist_name": Artist.get_by_id(self.artist_id)
        }


class Playlist(SqlAlchemyBase):
    __tablename__ = 'playlist'

    playlist_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    content = Column(PickleType, nullable=True)
    owner_id = Column(Integer, ForeignKey('user.user_id'), index=True, nullable=False)

    def to_dict(self, include_tracks=False):
        tracks = []
        if include_tracks and self.content is not None:
            s = create_session()
            for i in self.content:
                tracks.append(s.query(Track).get(i).to_dict())
        return {
            "id": self.playlist_id,
            "name": self.name,
            "content": self.content,
            "owner_id": self.owner_id,
            "tracks": tracks
        }
