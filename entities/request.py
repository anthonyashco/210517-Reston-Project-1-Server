from __future__ import annotations
from datetime import datetime
from exceptions import PermissionDenied
from typing import List, Tuple


class Request():
    def __init__(self,
                 request_id: int = 0,
                 employee_id: int = None,
                 request_amount: float = None,
                 request_details: List[Tuple[int, str, datetime]] = [],
                 manager_id: int = None,
                 decision: bool = None,
                 transaction_time: datetime = None,
                 decision_time: datetime = None) -> None:
        self.id = request_id
        self.employee_id = employee_id
        self.request_amount = request_amount
        self.request_details = []
        for request in request_details:
            if type(request) == dict:
                if type(request["post_time"]) == str:
                    time = request["post_time"]
                    micro = time.rpartition("-")[0].rpartition(".")[2]
                    if len(micro) < 6:
                        micro = micro + "0" * (6 - len(micro))
                        time = (f"{time.rpartition('.')[0]}"
                                f".{micro}-{time.rpartition('-')[2]}")
                    request["post_time"] = datetime.fromisoformat(time)
                self.request_details.append(tuple(request.values()))
        self.manager_id = manager_id
        self.decision = decision
        self.transaction_time = transaction_time
        self.decision_time = decision_time

    def __str__(self) -> str:
        return (f"Request {self.id} (Employee {self.employee_id}) "
                f"Amt: {self.request_amount}. Status: {self.decision}")

    def add_comment(self, user_id: int, comment: str):
        self.request_details.append((user_id, comment, datetime.now()))

    def edit_comment(self, user_id: int, index: int, edit: str):
        original_poster = self.request_details[index][0]
        if user_id != original_poster:
            raise PermissionDenied
        self.request_details[index] = (user_id, edit, datetime.now())

    def read_comments(self):
        return [comment for comment in self.request_details]

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "request_amount": float(self.request_amount),
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
