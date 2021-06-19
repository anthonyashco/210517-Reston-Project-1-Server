from daos.user_dao import UserDAO
from entities.user import User
from utils.connection import Connection
from utils.password import Password

conn = Connection.conn


class LoginService():

    def __init__(self, user_dao: UserDAO):
        self.u = user_dao

    def login(self, email: str, password: str) -> str:
        with conn:
            with conn.cursor() as cursor:
                user: User = self.u.get_from_email(cursor, email)
                if Password.check_pass(password, user.pass_hash,
                                       user.pass_salt):
                    return user.encode_auth_token()
