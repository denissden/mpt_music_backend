import datetime

from flask import *
from werkzeug.security import generate_password_hash, check_password_hash
from database import db_session
from apps import functions
from database.models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/register')
def register():
    return render_template("register.html")


@auth.route("/register", methods=['POST'])
def register_post():
    email = request.form.get('email')
    login_ = request.form.get('login')
    password = request.form.get('password')

    if len(password) < 6:
        return "password is too short"

    if len(login_) > 16:
        return "login is too long"
    if len(login_) < 3:
        return "login is too short"
    if not functions.check_login(login_):
        return "incorrect login"

    if not functions.check_email(email):
        return "incorrect email"

    s = db_session.create_session()

    # email exists
    if s.query(User).filter(User.email == email).scalar() is not None:
        s.close()
        return "email already exists"

    # email exists
    if s.query(User).filter(User.login == login_).scalar() is not None:
        s.close()
        return "login already exists"

    new_user = User(email=email,
                    login=login_,
                    password=generate_password_hash(password, method="sha512"),
                    created_date=datetime.datetime.now())

    s.add(new_user)
    s.commit()

    return "success"


@auth.route("/login", methods=['POST'])
def login_post():
    login_ = request.form.get('login')
    password = request.form.get('password')

    s = db_session.create_session()

    if functions.check_email(login_):
        user = s.query(User).filter(User.email == login_).first()
    elif functions.check_login(login_):
        user = s.query(User).filter(User.login == login_).first()
    else:
        return "Incorrect login"

    if not user or not check_password_hash(user.password, password):
        return "Incorrect email/login or password"

    login_user(user, remember=True)
    return "success"


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return "success"
