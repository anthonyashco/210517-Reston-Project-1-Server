from daos.file_dao import FileDAO
from daos.request_dao import RequestDAO
from daos.user_dao import UserDAO
from datetime import datetime
from entities.file import File
from entities.request import Request
from entities.user import User
from typing import List, Tuple
from utils.connection import Connection
from utils.password import Password

conn = Connection.conn


class ManagerService():

    def __init__(self, file_dao: FileDAO, request_dao: RequestDAO,
                 user_dao: UserDAO):
        self.f = file_dao
        self.r = request_dao
        self.u = user_dao

    def get_user(self, user_id: int) -> User:
        with conn:
            with conn.cursor() as cursor:
                return self.u.get_from_id(cursor, user_id)

    def create_user(self, user: User) -> User:
        with conn:
            with conn.cursor() as cursor:
                return self.u.create(cursor, user)

    def create_user_inline(self, email: str, password: str, first_name: str,
                           last_name: str, status: str) -> User:
        pass_hash, pass_salt = Password.hash_griddle(password)
        with conn:
            with conn.cursor() as cursor:
                return self.u.create(
                    cursor,
                    User(0, email, pass_hash, pass_salt, first_name, last_name,
                         status))

    def edit_user(self, user: User) -> User:
        with conn:
            with conn.cursor() as cursor:
                return self.u.update(cursor, user)

    def get_requests(self) -> List[Request]:
        with conn:
            with conn.cursor() as cursor:
                return self.r.get_all(cursor)

    def get_pending(self) -> List[Request]:
        with conn:
            with conn.cursor() as cursor:
                return self.r.get_pending(cursor)

    def get_completed(self) -> List[Request]:
        with conn:
            with conn.cursor() as cursor:
                return self.r.get_completed(cursor)

    def get_request(self, req_id: int):
        with conn:
            with conn.cursor() as cursor:
                return self.r.get_from_id(cursor, req_id)

    def edit_request(self, request: Request) -> Request:
        with conn:
            with conn.cursor() as cursor:
                return self.r.update(cursor, request)

    def add_comment(self, request: Request, user_id: int,
                    comment: str) -> Request:
        request.add_comment(user_id, comment)
        return self.edit_request(request)

    def edit_comment(self, request: Request, user_id: int, index: int,
                     edit: str) -> Request:
        request.edit_comment(user_id, index, edit)
        return self.edit_request(request)

    def read_comments(self,
                      request: Request) -> List[Tuple[int, str, datetime]]:
        return request.read_comments()

    def get_filenames_from_request(self, request_id: int) -> List[str]:
        with conn:
            with conn.cursor() as cursor:
                return self.f.get_filenames_from_request_id(cursor, request_id)

    def get_file(self, file_id: int) -> File:
        with conn:
            with conn.cursor() as cursor:
                return self.f.get_from_id(cursor, file_id)

    def read_request(self, request_id: int) -> Tuple[Request, List[File]]:
        with conn:
            with conn.cursor() as cursor:
                request = self.r.get_from_id(cursor, request_id)
                files = self.f.get_from_request_id(cursor, request_id)
                return request, files

    def update_request(self, request: Request) -> Request:
        with conn:
            with conn.cursor() as cursor:
                return self.r.update(cursor, request)

    # TODO Statistics page
