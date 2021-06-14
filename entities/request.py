from __future__ import annotations
from datetime import datetime


class Request():

    def __init__(self,
                 request_id: int = 0,
                 employee_id: int = None,
                 request_amount: float = None,
                 request_details: str = None,
                 manager_id: int = None,
                 decision: bool = None,
                 transaction_time: datetime = None,
                 decision_time: datetime = None) -> None:
        self.id = request_id
        self.employee_id = employee_id
        self.request_amount = request_amount
        self.request_details = request_details
        self.manager_id = manager_id
        self.decision = decision
        self.transaction_time = transaction_time
        self.decision_time = decision_time

    def __str__(self) -> str:
        return (f"Request {self.id} (Employee {self.employee_id}) "
                f"Amt: {self.request_amount}. Status: {self.decision}")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "request_amount": self.request_amount,
            "request_details": self.request_details,
            "manager_id": self.manager_id,
            "decision": self.decision,
            "transaction_time": self.transaction_time,
            "decision_time": self.decision_time
        }

    @staticmethod
    def from_json(json: dict) -> Request:
        return Request(json["id"], json["employee_id"], json["request_amount"],
                       json["request_details"], json["manager_id"],
                       json["decision"], json["transaction_time"],
                       json["decision_time"])
