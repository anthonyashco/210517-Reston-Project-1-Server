from entities.file import File
from exceptions import ResourceNotFound
from typing import List


class FileDAO():

    @staticmethod
    def create(cursor, file: File) -> File:
        smt = """\
            insert into
                expense.file
            values
                (default, %s, %s, %s, %s, %s, %s)
            returning
                id"""
        cursor.execute(smt, [
            file.employee_id, file.request_id, file.filename, file.ext,
            file.uploaded, file.upload_time
        ])
        file.id = cursor.fetchone()[0]
        return file

    @staticmethod
    def get_from_id(cursor, file_id: int) -> File:
        smt = "select * from expense.file where id = %s"
        cursor.execute(smt, [file_id])
        records = cursor.fetchall()
        files = [File(*record) for record in records]
        if len(files) == 0:
            raise ResourceNotFound(f"File with id {file_id} not found.")
        return files[0]

    @staticmethod
    def get_from_request_id(cursor, request_id: int) -> File:
        smt = "select * from expense.file where request_id = %s"
        cursor.execute(smt, [request_id])
        records = cursor.fetchall()
        files = [File(*record) for record in records]
        if len(files) == 0:
            raise ResourceNotFound(
                f"File with request id {request_id} not found.")
        return files[0]

    @staticmethod
    def get_all(cursor) -> List[File]:
        smt = "select * from expense.file"
        cursor.execute(smt)
        records = cursor.fetchall()
        files = [File(*record) for record in records]
        return files

    @staticmethod
    def update(cursor, file: File) -> File:
        smt = """\
            update
                expense.file
            set
                employee_id = %s, request_id = %s, filename = %s,
                ext = %s, uploaded = %s, upload_time = %s
            where
                id = %s"""
        cursor.execute(smt, [
            file.employee_id, file.request_id, file.filename, file.ext,
            file.uploaded, file.upload_time, file.id
        ])
        if cursor.rowcount == 0:
            raise ResourceNotFound(f"File with id of {file.id} not found.")
        return file

    @staticmethod
    def delete(cursor, file: File) -> bool:
        smt = "delete from expense.file where id = %s"
        cursor.execute(smt, [file.id])
        return True if cursor.rowcount > 0 else False
