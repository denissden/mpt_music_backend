from flask import *
from database import db_session
from flask_login import LoginManager

import os

absp = os.path.abspath  # shorter abspath

DIR = os.getcwd()


def create_app():
    app = Flask(__name__)

    # setup with the configuration provided
    app.config.from_object('config.DevelopmentConfig')
    print(os.getcwd())
    db_session.global_init(absp("database/data.sqlite/"))  # init database

    #############
    # init apps #
    #############

    # stream
    from apps.stream.views import stream
    app.register_blueprint(stream)

    # authentication
    from apps.auth.views import auth
    app.register_blueprint(auth)

    # api
    from apps.api.views import api
    app.register_blueprint(api, url_prefix="/api")

    ##################
    # authentication #
    ##################

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    ############
    # database #
    ############

    from database.models import User

    @login_manager.user_loader
    def load_user(user_id):
        s = db_session.create_session()
        user = s.query(User).filter(User.user_id == user_id).first()
        s.close()
        return user

    # not a good idea to define a function inside another function
    @app.route('/favicon.ico')
    def favicon():
        return redirect(url_for('static', filename='favicon.ico'))

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    create_app().run(host='0.0.0.0', port=port)
