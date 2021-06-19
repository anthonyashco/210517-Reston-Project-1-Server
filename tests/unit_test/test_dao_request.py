from copy import copy
from daos.user_dao import UserDAO as u
from daos.request_dao import RequestDAO as r
from datetime import datetime
from entities.user import User
from entities.request import Request
from exceptions import ResourceNotFound
from utils.connection import Connection
import pytest

USER_1 = User(None, "test_1@fake.email", "153417bd132637ba71cf236c323a55bd",
              "71a8b28bf9986f51ab5e31c1c20993f3", "Testy", "McTestFace",
              "employee")
USER_2 = User(None, "test_2@fake.email", "153417bd132637ba71cf236c323a55bd",
              "71a8b28bf9986f51ab5e31c1c20993f3", "Bossy", "McBossFace",
              "manager")
REQUEST_1 = Request(None, 0, 200.00,
                    [(0, "I can haz reimburse for laptop?", datetime.now())],
                    None, None, None, None)
REQUEST_2 = Request(
    None, 0, 5.00,
    [(0, "Venti iced caramel macchiato for the meeting.", datetime.now())],
    None, None, None, None)
conn = Connection.conn


def test_create():
    with conn:
        with conn.cursor() as cursor:
            user = copy(USER_1)
            user = u.create(cursor, user)
            assert user.id is not None

            request = copy(REQUEST_1)
            request.employee_id = user.id
            request = r.create(cursor, request)
            assert request.id is not None
            assert request.employee_id == user.id
            conn.rollback()


def test_comments():
    with conn:
        with conn.cursor() as cursor:
            user = copy(USER_1)
            user = u.create(cursor, user)
            request = copy(REQUEST_1)
            request.employee_id = user.id
            request = r.create(cursor, request)
            request.add_comment(user.id, "Pretty please?")
            request = r.update(cursor, request)
            request.edit_comment(user.id, 1, "Pretty please with sugar on top?")
            request = r.update(cursor, request)
            comments = request.read_comments()
            assert comments[0][1] == "I can haz reimburse for laptop?"
            assert comments[1][1] == "Pretty please with sugar on top?"
            conn.rollback()


def test_approve():
    with conn:
        with conn.cursor() as cursor:
            user = copy(USER_1)
            user = u.create(cursor, user)
            request = copy(REQUEST_1)
            request.employee_id = user.id
            request = r.create(cursor, request)

            manager = copy(USER_2)
            manager = u.create(cursor, manager)
            request.manager_id = manager.id
            request.decision = True
            request.decision_time = datetime.now()
            request = r.update(cursor, request)
            update = r.get_from_id(cursor, request.id)
            assert update.manager_id == manager.id
            conn.rollback()


def test_delete():
    with conn:
        with conn.cursor() as cursor:
            user = copy(USER_1)
            user = u.create(cursor, user)
            request = copy(REQUEST_1)
            request.employee_id = user.id
            request = r.create(cursor, request)
            r.delete(cursor, request)
            with pytest.raises(ResourceNotFound):
                r.get_from_id(cursor, request.id)
            conn.rollback()
