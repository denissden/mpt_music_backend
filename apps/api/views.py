from flask import Flask, Response, Blueprint, request
from flask_login import *
from database import db_session, models
from apps import functions
import os

api = Blueprint('api', __name__)


@api.route("/music/<music_id>")
def music_info(music_id):
    music_id = int(music_id)

    m = models.Track(id=music_id)
    return m.to_dict()


@api.route("/artist/<artist_id>")
def artist_info(artist_id):
    artist_id = int(artist_id)


@api.route("/add_music", methods=['POST'])
def add_music():
    # if current_user.artist_id is None:
    #     return 'you are not an artist'

    files_list = request.files
    if len(files_list) != 1:
        return 'wrong amount of files'

    file = files_list[next(files_list)]
    filename = functions.secure_filename(file.filename)
    if not filename.endswith(".mp3"):
        return 'not mp3'

    s = db_session.create_session()
    t = models.Track(name=filename, artist_id=current_user.artist_id)
    s.add(t)
    s.commit()

    file.save(os.path.join("audio", f"{t.track_id}.mp3"))

    return 'success'
