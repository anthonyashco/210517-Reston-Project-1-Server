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
                (default, %s, %s, %s, %s, %s, %s, %s)
            returning
                id"""
        cursor.execute(smt, [
            request.employee_id, request.request_amount,
            request.request_details, request.manager_id, request.decision,
            request.transaction_time, request.decision_time
        ])
        request.id = cursor.fetchone()[0]
        return request

    @staticmethod
    def get_from_id(cursor, request_id: int) -> Request:
        smt = "select * from expense.request where id = %s"
        cursor.execute(smt, [request_id])
        records = cursor.fetchall()
        requests = [Request(*record) for record in records]
        if len(requests) == 0:
            raise ResourceNotFound(f"Request with id {request_id} not found.")
        return requests[0]

    @staticmethod
    def get_from_manager_id(cursor, manager_id: int) -> Request:
        smt = "select * from expense.request where manager_id = %s"
        cursor.execute(smt, [manager_id])
        records = cursor.fetchall()
        requests = [Request(*record) for record in records]
        if len(requests) == 0:
            raise ResourceNotFound(
                f"Request with manager id {manager_id} not found.")
        return requests[0]

    @staticmethod
    def get_all(cursor) -> List[Request]:
        smt = "select * from expense.request"
        cursor.execute(smt)
        records = cursor.fetchall()
        requests = [Request(*record) for record in records]
        return requests

    @staticmethod
    def update(cursor, request: Request) -> Request:
        smt = """\
            update
                expense.request
            set
                employee_id = %s, request_amount = %s, request_details = %s,
                manager_id = %s, decision = %s, transaction_time = %s,
                decision_time = %s
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
