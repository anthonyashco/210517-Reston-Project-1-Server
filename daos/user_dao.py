from entities.user import User
from exceptions import ResourceNotFound
from typing import List


class UserDAO():

    @staticmethod
    def create(cursor, user: User) -> User:
        smt = """\
            insert into
                expense.user
            values
                (default, %s, %s, %s, %s, %s, %s)
            returning
                id"""
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status
        ])
        user.id = cursor.fetchone()[0]
        return user

    @staticmethod
    def get_from_id(cursor, user_id: int) -> User:
        smt = "select * from expense.user where id = %s"
        cursor.execute(smt, [user_id])
        records = cursor.fetchall()
        users = [User(*record) for record in records]
        if len(users) == 0:
            raise ResourceNotFound(f"User with id {user_id} not found.")
        return users[0]

    @staticmethod
    def get_from_email(cursor, email: str) -> User:
        smt = "select * from expense.user where email = %s"
        cursor.execute(smt, [email])
        records = cursor.fetchall()
        users = [User(*record) for record in records]
        if len(users) == 0:
            raise ResourceNotFound(f"User with email {email} not found.")
        return users[0]

    @staticmethod
    def get_all(cursor) -> List[User]:
        smt = "select * from expense.user"
        cursor.execute(smt)
        records = cursor.fetchall()
        users = [User(*record) for record in records]
        return users

    @staticmethod
    def update(cursor, user: User) -> User:
        smt = """\
            update
                expense.user
            set
                email = %s, pass_hash = %s, pass_salt = %s,
                first_name = %s, last_name = %s, status = %s
            where
                id = %s"""
        cursor.execute(smt, [
            user.email, user.pass_hash, user.pass_salt, user.first_name,
            user.last_name, user.status, user.id
        ])
        if cursor.rowcount == 0:
            raise ResourceNotFound(f"User with id of {user.id} not found.")
        return user

    @staticmethod
    def delete(cursor, user: User) -> bool:
        smt = "delete from expense.user where id = %s"
        cursor.execute(smt, [user.id])
        return True if cursor.rowcount > 0 else False
