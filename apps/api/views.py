from flask import Flask, Response, Blueprint, request
from flask_login import current_user, login_required
from database import db_session, models
from apps import functions
import json
import os

api = Blueprint('api', __name__)


@api.route("/track/<track_id>")
def music_info(track_id):
    track_id = int(track_id)
    s = db_session.create_session()
    t = s.query(models.Track).filter(models.Track.track_id == track_id).first()
    if t is not None:
        return t.to_dict()
    else:
        return "fail"


@api.route("/artist/<artist_id>")
def artist_info(artist_id):
    artist_id = int(artist_id)


@login_required
@api.route("/upload_track", methods=['POST'])
def add_music():
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


@login_required
@api.route("/create_playlist", methods=['POST'])
def create_playlist():
    playlist_name = request.form.get('name')
    if len(playlist_name) < 1:
        return 'name is too short'
    elif len(playlist_name) > 128:
        return 'name is too long'

    s = db_session.create_session()
    p = models.Playlist(name=playlist_name, owner_id=current_user.user_id)
    s.add(p)
    s.commit()

    return p.to_dict()


@login_required
@api.route("/all_playlists", methods=['GET'])
def load_playlists():
    s = db_session.create_session()
    res = s.query(models.Playlist).filter(models.Playlist.owner_id == current_user.user_id)
    return json.dumps([p.to_dict(True) for p in res]) if res is not None else None


@login_required
@api.route("/playlist/<playlist_id>", methods=['GET'])
def get_playlist(playlist_id):
    playlist_id = int(playlist_id)
    s = db_session.create_session()
    p = models.Playlist.query.get(playlist_id)

    return p.to_dict()


@login_required
@api.route("/add_to_playlist", methods=['POST'])
def add_to_playlist():
    playlist_id = int(request.form.get('playlist_id'))
    track_id = int(request.form.get('track_id'))

    s = db_session.create_session()
    p = models.Playlist.query.get(playlist_id)
    if p.owner_id == current_user.user_id:
        if p.content is None:
            p.content = []
        if models.Track.query.get(track_id) is not None:
            p.content.append(track_id)
            return "success"
        else:
            return "track does not exist"
    else:
        return "you are not the owner of the playlist"


@login_required
@api.route("/search_tracks", methods=['POST'])
def search_tracks():
    search_string = request.form.get('string')

    s = db_session.create_session()
    tracks = s.query(models.Track).filter(models.Track.login.like(search_string + "%"))
    return json.load([t.to_dict])

