from entities.user import User
from utils.app import app

USER = User(0, "test_1@fake.email", "153417bd132637ba71cf236c323a55bd",
            "71a8b28bf9986f51ab5e31c1c20993f3", "Testy", "McTestFace",
            "employee")


def test_auth_token():
    with app.app_context():
        token = USER.encode_auth_token()
    assert type(token) == str


def test_token_decode():
    with app.app_context():
        encode = USER.encode_auth_token()
        decode = USER.decode_auth_token(encode)
    assert decode == USER.id
