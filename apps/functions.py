import re
from database.models import User
from database.db_session import create_session
from sqlalchemy import or_, and_, literal

email_pattern = \
    re.compile(
        r"""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")


login_pattern = \
    re.compile(
        r"""(?:[a-zA-Z0-9_-]+$)""")


def check_email(email):
    return email_pattern.match(email)


def check_login(login):
    return login_pattern.match(login) and len(login) <= 16


def secure_filename(name):
    for c in ["/", "\\"]:
        name = name.replace(c, "_")
    return name


def get_last_id():
    s = create_session()
    query = s.query(User).order_by(User.user_id.desc()).first()
    if query is not None:
        return query.user_id
    return 0


def id_exists(user_id):
    return 0 < user_id <= get_last_id()


def search_login(pattern):
    s = create_session()
    users = s.query(User).filter(User.login.like(pattern + "%"))
    return users