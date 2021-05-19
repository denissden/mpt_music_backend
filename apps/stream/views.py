from flask import Flask, Response, Blueprint, request
from flask_login import login_required
from database import db_session, models
from apps import functions
import os

stream = Blueprint('stream', __name__)


@login_required
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
