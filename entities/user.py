from __future__ import annotations
from datetime import datetime, timedelta
from flask import current_app
import jwt


class User():
    def __init__(self,
                 user_id: int = 0,
                 email: str = None,
                 pass_hash: str = None,
                 pass_salt: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 status: str = None) -> None:
        self.id = user_id
        self.email = email
        self.pass_hash = pass_hash
        self.pass_salt = pass_salt
        self.first_name = first_name
        self.last_name = last_name
        self.status = status

    def __str__(self) -> str:
        return f"User {self.id} ({self.email}). Status: {self.status}"

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "email": self.email,
            "pass_hash": self.pass_hash,
            "pass_salt": self.pass_salt,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status
        }

    def encode_auth_token(self) -> str:
        payload = {
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow(),
            "sub": self.id,
        }
        try:
            return jwt.encode(payload,
                              current_app.config["SECRET_KEY"],
                              algorithm="HS256")
        except Exception as e:
            print(e)

    @staticmethod
    def decode_auth_token(auth_token: str):
        payload = jwt.decode(auth_token,
                             current_app.config["SECRET_KEY"],
                             algorithms=["HS256"])
        return payload["sub"]

    @staticmethod
    def from_json(json: dict) -> User:
        return User(json["id"], json["email"], json["pass_hash"],
                    json["pass_salt"], json["first_name"], json["last_name"],
                    json["status"])
