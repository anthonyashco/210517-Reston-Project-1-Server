from __future__ import annotations
from datetime import datetime


class File():

    def __init__(self,
                 file_id: int = 0,
                 employee_id: int = None,
                 request_id: int = None,
                 filename: str = None,
                 ext: str = None,
                 uploaded: bytes = None,
                 upload_time: datetime = None) -> None:
        self.id = file_id
        self.employee_id = employee_id
        self.request_id = request_id
        self.filename = filename
        self.ext = ext
        self.uploaded = uploaded
        self.upload_time = upload_time

    def __str__(self) -> str:
        return (f"File {self.id} "
                f"(Employee {self.employee_id}, Request {self.request_id}) "
                f"{self.filename}.{self.ext}")

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "employee_id": self.employee_id,
            "request_id": self.request_id,
            "filename": self.filename,
            "ext": self.ext,
            "uploaded": self.uploaded,
            "upload_time": self.upload_time,
        }

    @staticmethod
    def from_json(json: dict) -> File:
        return File(json["id"], json["employee_id"], json["request_id"],
                    json["filename"], json["ext"], json["uploaded"],
                    json["upload_time"])
