from daos.user_dao import UserDAO as u
from entities.user import User
from exceptions import ResourceNotFound
from utils.connection import Connection
import pytest

USER_1 = User(None, "test_1@fake.email", "153417bd132637ba71cf236c323a55bd",
              "71a8b28bf9986f51ab5e31c1c20993f3", "Testy", "McTestFace",
              "employee")
USER_2 = User(None, "test_2@fake.email", "153417bd132637ba71cf236c323a55bd",
              "71a8b28bf9986f51ab5e31c1c20993f3", "Bossy", "McBossFace",
              "manager")
conn = Connection.conn


def test_create():
    with conn:
        with conn.cursor() as cursor:
            created = u.create(cursor, USER_1)
            assert created.id is not None
            conn.rollback()


def test_get_from_email():
    with conn:
        with conn.cursor() as cursor:
            u.create(cursor, USER_1)
            email = u.get_from_email(cursor, "test_1@fake.email")
            assert email.first_name == "Testy"
            conn.rollback()


def test_get_all():
    with conn:
        with conn.cursor() as cursor:
            u.create(cursor, USER_1)
            u.create(cursor, USER_2)
            users = u.get_all(cursor)
            assert len(users) > 1
            assert type(users[0]) == User
            conn.rollback()


def test_update():
    with conn:
        with conn.cursor() as cursor:
            updated = u.create(cursor, USER_1)
            updated.status = "closed"
            u.update(cursor, updated)
            updated_2 = u.get_from_id(cursor, updated.id)
            assert updated_2.status == "closed"
            conn.rollback()


def test_delete():
    with conn:
        with conn.cursor() as cursor:
            deleted = u.create(cursor, USER_1)
            u.delete(cursor, deleted)
            with pytest.raises(ResourceNotFound):
                u.get_from_id(cursor, deleted.id)
            conn.rollback()
