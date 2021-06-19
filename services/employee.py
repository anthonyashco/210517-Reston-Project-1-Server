from exceptions import PermissionDenied
from daos.file_dao import FileDAO
from daos.request_dao import RequestDAO
from daos.user_dao import UserDAO
from datetime import datetime
from entities.file import File
from entities.request import Request
from entities.user import User
from typing import List, Tuple
from utils.connection import Connection

conn = Connection.conn


class EmployeeService():

    def __init__(self, file_dao: FileDAO, request_dao: RequestDAO,
                 user_dao: UserDAO):
        self.f = file_dao
        self.r = request_dao
        self.u = user_dao

    def get_user(self, user_id: int) -> User:
        with conn:
            with conn.cursor() as cursor:
                return self.u.get_from_id(cursor, user_id)

    def create_request(self, request: Request) -> Request:
        with conn:
            with conn.cursor() as cursor:
                return self.r.create(cursor, request)

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

    def get_user_specific_request(self, usr_id: int, req_id: int) -> Request:
        with conn:
            with conn.cursor() as cursor:
                req = self.r.get_from_id(cursor, req_id)
                if req.employee_id != usr_id:
                    raise PermissionDenied
                else:
                    return req

    def get_requests_from_uid(self, user_id: int) -> List[Request]:
        with conn:
            with conn.cursor() as cursor:
                return self.r.get_from_user_id(cursor, user_id)

    def attach_file(self, file: File) -> File:
        with conn:
            with conn.cursor() as cursor:
                return self.f.create(cursor, file)

    def get_filenames_from_request(self, request_id: int) -> List[str]:
        with conn:
            with conn.cursor() as cursor:
                return self.f.get_filenames_from_request_id(cursor, request_id)

    def get_user_specific_file(self, user_id: int, file_id: int) -> File:
        with conn:
            with conn.cursor() as cursor:
                file = self.f.get_from_id(cursor, file_id)
                if file.employee_id != user_id:
                    raise PermissionDenied
                else:
                    return file
