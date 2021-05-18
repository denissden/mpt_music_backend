from flask import Flask, Response, Blueprint, request
from flask_login import *
from database import db_session, models
from apps import functions
import os

stream = Blueprint('stream', __name__)


@stream.route("/music/<music_id>")
def stream_music(music_id):
    music_id = int(music_id)

    def generate():
        with open(f"audio/{music_id}.mp3", "rb") as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)
    return Response(generate(), mimetype="audio/mpeg")


@stream.route("/music_info/<music_id>")
def music_info(music_id):
    music_id = int(music_id)

    m = models.Track(id=music_id)
    return m.to_dict()


@login_required
@stream.route("/add_music", methods=['POST'])
def add_music():
    if current_user.artist_id is None:
        return 'you are not an artist'

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
