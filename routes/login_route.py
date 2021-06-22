from daos.user_dao import UserDAO
from flask import Flask, jsonify, request
from services.login import LoginService
import json

l = LoginService(UserDAO)  # noqa: E741


def create_routes(app: Flask):
    @app.route("/")
    def hello():
        return "Hello!", 200

    @app.route("/login", methods=["POST"])
    def login() -> str:
        body = json.loads(request.data.decode("utf-8"))
        token = l.login(body["email"], body["password"])
        return jsonify(token)
