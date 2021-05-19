from flask import Flask, Response, Blueprint, request
from flask_login import current_user, login_required
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


@login_required
@api.route("/upload_track", methods=['POST'])
def add_music():
    print(request.files)
    print(request.form)
    track_name = request.form.get('name')
    artist_id = request.form.get('artist_id')

    if len(track_name) < 1:
        return "name is too short"

    if len(track_name) > 128:
        return "name is too long"

    files_list = request.files
    if len(files_list) != 1:
        return 'wrong amount of files'

    file = files_list['track']
    filename = functions.secure_filename(file.filename)
    if not filename.endswith(".mp3"):
        return 'file is not .mp3'

    s = db_session.create_session()
    t = models.Track(name=track_name,
                     artist_id=artist_id,
                     uploaded_id=current_user.user_id)
    s.add(t)
    s.commit()
    if t.track_id is not None:
        file.save(os.path.join("audio", f"{t.track_id}.mp3"))
    print(t.track_id)
    return 'success'
