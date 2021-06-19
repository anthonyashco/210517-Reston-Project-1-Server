from daos.user_dao import UserDAO
from entities.user import User
from services.login import LoginService
from utils.app import app
from utils.connection import Connection

conn = Connection.conn

l = LoginService(UserDAO)  # noqa: E741


def test_login():
    with app.app_context():
        token = l.login("employee@email.com", "password")
    assert type(token) == str


def test_token():
    with app.app_context():
        token = l.login("employee@email.com", "password")
        uid = User.decode_auth_token(token)
    assert type(uid) == int
