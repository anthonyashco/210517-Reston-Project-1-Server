from copy import copy
from daos.file_dao import FileDAO as f
from daos.request_dao import RequestDAO as r
from daos.user_dao import UserDAO as u
from entities.file import File
from entities.request import Request
from entities.user import User
from utils.connection import Connection

USER = User(None, "test_1@fake.email", "153417bd132637ba71cf236c323a55bd",
            "71a8b28bf9986f51ab5e31c1c20993f3", "Testy", "McTestFace",
            "employee")
REQUEST = Request(None, 0, 200.00, "Cute Raichu NFT", None, None, None, None)

with open("tests/files/raichu_stretch.gif", "rb") as x:
    filename = x.name.rpartition("/")[2].rpartition(".")[0]
    ext = x.name.rpartition(".")[2]
    FILE = File(filename=filename, ext=ext, uploaded=x.read())

conn = Connection.conn


def test_create():
    with conn:
        with conn.cursor() as cursor:
            user = u.create(cursor, USER)
            request = copy(REQUEST)
            request.employee_id = user.id
            request = r.create(cursor, request)
            file = copy(FILE)
            file.employee_id = user.id
            file.request_id = request.id
            file = f.create(cursor, file)
            image = f.get_from_id(cursor, file.id)
            assert f"{image.filename}.{image.ext}" == "raichu_stretch.gif"
            conn.rollback()
