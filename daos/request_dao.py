from entities.request import Request
from exceptions import ResourceNotFound
from typing import List


class RequestDAO():

    @staticmethod
    def create(cursor, request: Request) -> Request:
        smt = """\
            insert into
                expense.request
            values
                (default, %s, %s, %s::expense.detail_entry[], %s, %s, default, %s)
            returning
                id, transaction_time"""
        cursor.execute(smt, [
            request.employee_id, request.request_amount,
            request.request_details, request.manager_id, request.decision,
            request.decision_time
        ])
        result = cursor.fetchone()
        request.id = result[0]
        request.transaction_time = result[1]
        return request

    @staticmethod
    def get_from_id(cursor, request_id: int) -> Request:
        smt = """select row_to_json(row) from
            (select * from expense.request where id = %s) row"""
        cursor.execute(smt, [request_id])
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        if len(requests) == 0:
            raise ResourceNotFound(f"Request with id {request_id} not found.")
        return requests[0]

    @staticmethod
    def get_from_manager_id(cursor, manager_id: int) -> List[Request]:
        smt = """select row_to_json(row) from
            (select * from expense.request where manager_id = %s) row"""
        cursor.execute(smt, [manager_id])
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        if len(requests) == 0:
            raise ResourceNotFound(
                f"Request with manager id {manager_id} not found.")
        return requests

    @staticmethod
    def get_from_user_id(cursor, user_id: int) -> List[Request]:
        smt = """select row_to_json(row) from
            (select * from expense.request where employee_id = %s) row"""
        cursor.execute(smt, [user_id])
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        if len(requests) == 0:
            raise ResourceNotFound(
                f"Request with employee id {user_id} not found.")
        return requests

    @staticmethod
    def get_all(cursor) -> List[Request]:
        smt = """select row_to_json(row) from
            (select * from expense.request) row"""
        cursor.execute(smt)
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        return requests

    @staticmethod
    def get_pending(cursor) -> List[Request]:
        smt = """select row_to_json(row) from
            (select * from expense.request where decision is null) row"""
        cursor.execute(smt)
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        return requests

    @staticmethod
    def get_completed(cursor) -> List[Request]:
        smt = """select row_to_json(row) from
            (select * from expense.request where decision is not null) row"""
        cursor.execute(smt)
        records = cursor.fetchall()
        requests = [Request(*record[0].values()) for record in records]
        return requests

    @staticmethod
    def update(cursor, request: Request) -> Request:
        smt = """\
            update
                expense.request
            set
                employee_id = %s, request_amount = %s,
                request_details = %s::expense.detail_entry[], manager_id = %s,
                decision = %s, transaction_time = %s, decision_time = %s
            where
                id = %s"""
        cursor.execute(smt, [
            request.employee_id, request.request_amount,
            request.request_details, request.manager_id, request.decision,
            request.transaction_time, request.decision_time, request.id
        ])
        if cursor.rowcount == 0:
            raise ResourceNotFound(
                f"Request with id of {request.id} not found.")
        return request

    @staticmethod
    def delete(cursor, request: Request) -> bool:
        smt = "delete from expense.request where id = %s"
        cursor.execute(smt, [request.id])
        return True if cursor.rowcount > 0 else False
